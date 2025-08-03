from test_class import Animal
from test_class  import Species


def insert_animal_name():
    while len(Animal.saved_names) < 2:
        name = input("Enter the animal name: ")
        animal = Animal(name)
        animal.save_name()
    return Animal.saved_names
        

def insert_species_name():
    while len(Species.saved_species) < 2:
        species_name = input("Enter the species name: ")
        species = Species(species_name)
        species.save_species()
    return Species.saved_species



def animal_to_species():
    if len(insert_animal_name()) == len(insert_species_name()):
        question = input("which animal you would like to see the species of? ")
        if question in insert_animal_name():
            index = insert_animal_name().index(question)
            print(insert_species_name()[index])
        else:
            print("Animal not found.")

insert_animal_name()
insert_species_name()
animal_to_species()




