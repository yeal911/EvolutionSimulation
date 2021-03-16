#!/usr/bin/python3
import Population
import Gene

class Wolf(Population):
    """this class defines the properties and behaviours of wolf population"""

    # lifespan
    lifespan = None

    # gender
    gender = None

    # hungry level
    hungryLevel = None

    # gene set
    geneSet = []

    # breeding times for each individual
    breedingTimes = 2

    # attack possibility
    attackPossibility = 8

    # defend possibility
    defendPossibility = 8

    # fight capability
    fightCapability = 8

    @classmethod  # static method of a class
    def populationName(cls):
        return "Wolf"

    def __init__(self, gene_set):
        self.geneSet = gene_set
        # add computation for properties based on gene set, each property has a base value.

    # forage behaviour of wolf
    def forage(self):


    # grow behaviour of a wolf
    def grow(self):


    # attack behaviour of a wolf
    def attack(self):


    # defend behaviour of a wolf
    def defend(self):


    # breed behaviour of a wolf
    def breed(self):


