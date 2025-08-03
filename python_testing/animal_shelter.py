import json
import os


class AnimalShelter:

    animals = []
    

    def __init__(self,animal_name, animal_species,age):
        self.animal_name = animal_name
        self.animal_species = animal_species
        self.age = age
    
    def add_animal(self):
        AnimalShelter.animals.append(self)

    def show_animal_list(self):
        if len(AnimalShelter.animals) == 0:
            print("No animals in the shelter.")
        else:
            print(self.animal_name + " " + self.animal_species + " " + self.age)

    def delete_animal(self):
        for animal in AnimalShelter.animals:
            if animal.animal_name == self.animal_name:
                AnimalShelter.animals.remove(animal)
                print(f"Animal {self.animal_name} deleted successfully.")
                return
        print("Animal not found.")
    
    def to_dict(self):
        return {
            "animal_name": self.animal_name,
            "animal_species": self.animal_species,
            "age": self.age
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["animal_name"], data["animal_species"], data["age"])

    @classmethod
    def save_to_json(cls, filename="animals.json"):
        with open(filename, 'w') as file:
            json.dump([animal.to_dict() for animal in cls.animals], file, indent=4)
        print(f"Animals saved to {filename} successfully.")

    @classmethod
    def load_from_json(cls, filename="animals.json"):   
        if not os.path.exists(filename):
            print(f"{filename} does not exist.")
            return
        with open(filename, 'r') as file:
            data = json.load(file)
            cls.animals = [cls.from_dict(animal) for animal in data]
        print(f"Animals loaded from {filename} successfully.")

def main():
    
    input_choice = input(
    "Enter 1 to add an animal\n"
    "Enter 2 to delete an animal\n"
    "Enter 3 to find an animal by name\n"
    "Enter 4 to list all animals\n"
    "Enter 5 to exit:\n"
    "Enter 6 to save animals to json:\n"
    "Enter 7 to load animals from json:\n")

    choice = int(input_choice)


    if choice == 1:
        name = input("Enter the animal name: ")
        species = input("Enter the animal species: ")
        age = input("Enter the animal age: ")
        animal = AnimalShelter(name, species, age)
        animal.add_animal()
    elif choice == 2:
        name = input("Enter the animal name to delete: ")
        animal = AnimalShelter(name, "", "")
        animal.delete_animal()
    elif choice == 3:
        name = input("Enter the animal name to find: ")
        found = False
        for animal in AnimalShelter.animals:
            if animal.animal_name == name:
                print(f"Animal found: {animal.animal_name}, Species: {animal.animal_species}, Age: {animal.age}")
                found = True
                break
        if not found:
            print("Animal not found.")
    elif choice == 4:
        if len(AnimalShelter.animals) == 0:
            print("No animals in the shelter.")
        else:
            print("Animals in the shelter:")
            for i in range(len(AnimalShelter.animals)):
                print(f"{AnimalShelter.animals[i].animal_name} - {AnimalShelter.animals[i].animal_species} - {AnimalShelter.animals[i].age}")
    elif choice == 5:
        print("Exiting the program.")
        exit()

    elif choice == 6:
        AnimalShelter.save_to_json()

    elif choice == 7:
        AnimalShelter.load_from_json()

    else: 
        print("Invalid choice. Please try again.")
        return main()

while True:
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        continue

