class Animal:
    saved_names = []

    def __init__(self, name):
        self.name = name
    
    def save_name(self):
        Animal.saved_names.append(self.name)
        



class Species:
    saved_species = []

    def __init__(self, species_name):
        self.species_name = species_name
    
    def save_species(self):

        Species.saved_species.append(self.species_name)

