import tkinter as tk
from tkinter import messagebox
import random
import math

class SquareMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Square Map Configurator")

        self.map_width = 8
        self.map_height = 8
        self.tile_size = 80
        self.tiles = {}
        self.tile_rects = set()
        self.text_to_tile = {}

        self.players = {}
        self.enemies = {}
        self.entity_id = 1
        self.selected_entity = None
        self.selection_outline = None

        self.battle_window = None
        self.battle_entries = []
        self.entities_backup = []  # pro zachování dat při resize

        self.create_widgets()
        self.root.bind("<Configure>", self.on_resize)

    def draw_map(self):
        self.entities_backup.clear()
        for tile in self.tiles:
            if self.tiles[tile]["entity"]:
                ent = self.tiles[tile]["entity"]
                self.entities_backup.append({
                    "x": self.tiles[tile]["x"],
                    "y": self.tiles[tile]["y"],
                    "label": ent["label"],
                    "color": ent["color"],
                    "hp": ent["hp"],
                    "kind": ent["kind"],
                    "weapon": ent.get("weapon"),
                    "armor": ent.get("armor")
                })

        self.canvas.delete("all")
        self.tiles.clear()
        self.text_to_tile.clear()
        self.tile_rects.clear()

        for y in range(self.map_height):
            for x in range(self.map_width):
                x1 = x * self.tile_size
                y1 = y * self.tile_size
                x2 = x1 + self.tile_size
                y2 = y1 + self.tile_size
                rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="")
                self.tiles[rect_id] = {
                    "x": x,
                    "y": y,
                    "center": ((x1 + x2) // 2, (y1 + y2) // 2),
                    "entity": None
                }
                self.tile_rects.add(rect_id)

        for entity in self.entities_backup:
            for tile in self.tiles:
                if self.tiles[tile]["x"] == entity["x"] and self.tiles[tile]["y"] == entity["y"]:
                    self.spawn_entity(tile, entity["label"], entity["color"], entity["hp"],
                                      entity["kind"], entity.get("weapon"), entity.get("armor"))
                    break

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        config_frame = tk.Frame(self.main_frame)
        config_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(config_frame, text="Počet hráčů (1-4):").pack()
        self.player_count_var = tk.IntVar(value=1)
        tk.Spinbox(config_frame, from_=1, to=4, textvariable=self.player_count_var).pack()

        tk.Button(config_frame, text="Umístit hráče (výběr)", command=self.place_players_manual).pack(pady=5)
        tk.Button(config_frame, text="Umístit hráče (náhodně)", command=self.place_players_random).pack(pady=5)

        tk.Label(config_frame, text="Počet nepřátel (1-6):").pack(pady=(10, 0))
        self.enemy_count_var = tk.IntVar(value=1)
        tk.Spinbox(config_frame, from_=1, to=6, textvariable=self.enemy_count_var).pack()

        tk.Label(config_frame, text="Max. životy nepřátel:").pack()
        self.enemy_hp_max_var = tk.IntVar(value=10)
        tk.Spinbox(config_frame, from_=1, to=99, textvariable=self.enemy_hp_max_var).pack()

        tk.Button(config_frame, text="Přidat nepřátele", command=self.place_enemies).pack(pady=5)
        tk.Button(config_frame, text="Souboj", command=self.open_battle_window).pack(pady=(20, 0))

        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.draw_map()

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def place_players_manual(self):
        self.remaining_players = self.player_count_var.get()
        self.root.config(cursor="hand2")
        self.canvas.bind("<Button-1>", self.manual_player_placement)

    def manual_player_placement(self, event):
        tile = self.get_tile_under_cursor(event.x, event.y)
        if tile and self.tiles[tile]["entity"] is None:
            color = ["red", "blue", "green", "orange"][self.entity_id - 1]
            self.spawn_entity(tile, f"P{self.entity_id}", color, 10, "player")
            self.entity_id += 1
            self.remaining_players -= 1
            if self.remaining_players == 0:
                self.canvas.bind("<Button-1>", self.on_canvas_click)
                self.root.config(cursor="")

    def place_players_random(self):
        player_count = self.player_count_var.get()
        positions = [tile for tile in self.tiles if self.tiles[tile]['x'] < self.map_width // 2 and self.tiles[tile]['entity'] is None]
        random.shuffle(positions)
        for i in range(player_count):
            color = ["red", "blue", "green", "orange"][i]
            self.spawn_entity(positions[i], f"P{i + 1}", color, 10, "player")
            self.entity_id += 1

    def place_enemies(self):
        count = self.enemy_count_var.get()
        hp_max = self.enemy_hp_max_var.get()
        positions = [tile for tile in self.tiles if self.tiles[tile]['x'] >= self.map_width // 2 and self.tiles[tile]['entity'] is None]
        random.shuffle(positions)
        for i in range(count):
            hp = random.randint(1, hp_max)
            weapon = random.choice(["ruce", "dýka", "meč", "luk", "sekyra"])
            armor = random.choice(["žádná", "lehká", "střední", "těžká"])
            self.spawn_entity(positions[i], f"N{i + 1}", "black", hp, "enemy", weapon, armor)

    def spawn_entity(self, tile, label, color, hp, kind, weapon=None, armor=None):
        if self.tiles[tile]["entity"]:
            self.canvas.delete(self.tiles[tile]["entity"]["id"])
            self.canvas.delete(self.tiles[tile]["entity"]["overlay"])

        center = self.tiles[tile]["center"]
        tile_coords = self.canvas.coords(tile)
        overlay_id = self.canvas.create_rectangle(
            tile_coords[0], tile_coords[1], tile_coords[2], tile_coords[3],
            fill=color, stipple="gray25", outline="")
        text_id = self.canvas.create_text(center[0], center[1], text=f"{label}\n{hp}HP", fill=color, font=("Arial", 10, "bold"))
        self.text_to_tile[text_id] = tile

        self.tiles[tile]["entity"] = {
            "id": text_id,
            "overlay": overlay_id,
            "label": label,
            "color": color,
            "hp": hp,
            "kind": kind,
            "tile": tile,
            "weapon": weapon,
            "armor": armor
        }

    def get_tile_under_cursor(self, x, y):
        clicked = self.canvas.find_closest(x, y)
        if not clicked:
            return None
        item = clicked[0]
        if item in self.tiles:
            return item
        elif item in self.text_to_tile:
            return self.text_to_tile[item]
        return None

    def on_canvas_click(self, event):
        tile = self.get_tile_under_cursor(event.x, event.y)
        if tile is None:
            return

        if self.selection_outline:
            self.canvas.delete(self.selection_outline)
            self.selection_outline = None

        if self.selected_entity:
            if self.tiles[tile]["entity"] is None:
                entity = self.selected_entity
                new_center = self.tiles[tile]["center"]
                self.canvas.coords(entity["id"], new_center[0], new_center[1])
                old_tile = entity["tile"]
                self.canvas.coords(entity["overlay"], self.canvas.coords(tile))
                self.tiles[old_tile]["entity"] = None
                self.tiles[tile]["entity"] = entity
                entity["tile"] = tile
                self.text_to_tile[entity["id"]] = tile
                self.selected_entity = None
            else:
                self.selected_entity = None
        elif self.tiles[tile]["entity"]:
            self.selected_entity = self.tiles[tile]["entity"]
            tile_coords = self.canvas.coords(tile)
            self.selection_outline = self.canvas.create_rectangle(
                tile_coords[0], tile_coords[1], tile_coords[2], tile_coords[3],
                outline="blue", width=3)

    def on_resize(self, event):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.tile_size = min(canvas_width // self.map_width, canvas_height // self.map_height)
        self.draw_map()

    def open_battle_window(self):
        if self.battle_window and self.battle_window.winfo_exists():
            self.battle_window.lift()
            return

        self.battle_window = tk.Toplevel(self.root)
        self.battle_window.title("Soubojový přehled")
        self.battle_window.protocol("WM_DELETE_WINDOW", self.close_battle_window)

        player_frame = tk.LabelFrame(self.battle_window, text="Hráči")
        player_frame.grid(row=0, column=0, padx=10, pady=10)

        enemy_frame = tk.LabelFrame(self.battle_window, text="Nepřátelé")
        enemy_frame.grid(row=0, column=1, padx=10, pady=10)

        self.battle_entries = []

        for tile, data in self.tiles.items():
            entity = data["entity"]
            if not entity:
                continue
            frame = player_frame if entity["kind"] == "player" else enemy_frame
            row = len(self.battle_entries)
            tk.Label(frame, text=entity["label"]).grid(row=row, column=0)
            hp_entry = tk.Entry(frame, width=5)
            hp_entry.grid(row=row, column=1)
            hp_entry.insert(0, str(entity["hp"]))
            armor_entry = tk.Entry(frame, width=10)
            armor_entry.grid(row=row, column=2)
            armor_entry.insert(0, str(entity.get("armor", "")))
            weapon_entry = tk.Entry(frame, width=10)
            weapon_entry.grid(row=row, column=3)
            weapon_entry.insert(0, str(entity.get("weapon", "")))
            self.battle_entries.append({
                "entity": entity,
                "hp": hp_entry,
                "armor": armor_entry,
                "weapon": weapon_entry
            })

        tk.Button(self.battle_window, text="Upravit hodnoty", command=self.update_battle_stats).grid(row=1, column=0, columnspan=2, pady=10)

    def close_battle_window(self):
        if self.battle_window:
            self.battle_window.destroy()
            self.battle_window = None

    def update_battle_stats(self):
        for entry in self.battle_entries:
            entity = entry["entity"]
            entity["hp"] = int(entry["hp"].get())
            entity["armor"] = entry["armor"].get()
            entity["weapon"] = entry["weapon"].get()
            self.canvas.itemconfig(entity["id"], text=f"{entity['label']}\n{entity['hp']}HP")
            self.entities_backup = [
                {
                    **e,
                    "hp": entity["hp"] if e["label"] == entity["label"] else e["hp"],
                    "armor": entity["armor"] if e["label"] == entity["label"] else e["armor"],
                    "weapon": entity["weapon"] if e["label"] == entity["label"] else e["weapon"]
                } for e in self.entities_backup
            ]

if __name__ == "__main__":
    root = tk.Tk()
    app = SquareMapApp(root)
    root.mainloop()
