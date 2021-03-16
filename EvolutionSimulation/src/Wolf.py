#!/usr/bin/python3
import random

import Population
import Gene


class Wolf(Population):
    """this class defines the properties and behaviours of wolf population"""
    # Gene count for wolf
    __geneCount = 10

    # lifespan
    lifespan = None

    # gender
    gender = None

    # hungry level
    hungryLevel = None

    # attack possibility
    attackPossibility = None

    # defend possibility
    defendPossibility = None

    # fight capability
    fightCapability = None

    # gene set
    geneSet = []

    # breeding times for each individual
    breedingTimes = 2

    @classmethod  # static method of a class
    def populationName(cls):
        return "Wolf"

    def __init__(self, gene_set):
        self.geneSet = gene_set
        # self.geneSet = []
        # initialize gene set
        i = 0
        while i < Wolf.__geneCount:
            self.geneSet.append(Gene())
            i += 1
        # initialize the property value, each property has a base value
        self.lifespan = 10
        self.fightCapability = 5
        genderGroup = ["M", "F"]
        self.gender = genderGroup[random.randint(0, 1)]
        self.attackPossibility = 5
        self.defendPossibility = 5
        self.hungryLevel = 5

        # add computation for properties based on gene set


    # forage behaviour of wolf
    # tesettttt
    def forage(self):
        return None

    # grow behaviour of a wolf
    def grow(self):
        return None

    # attack behaviour of a wolf
    def attack(self):
        return None

    # defend behaviour of a wolf
    def defend(self):
        return None

    # breed behaviour of a wolf
    def breed(self, father, mother):
        return None
