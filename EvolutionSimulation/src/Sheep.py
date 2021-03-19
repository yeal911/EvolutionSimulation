#!/usr/bin/python3
import random

from Population import Population
from Gene import Gene


class Sheep(Population):
    """this class defines the properties and behaviours of sheep population"""
    # Gene count for sheep
    __geneCount = 10

    # lower growth period
    lowerGrowthPeriod = 5

    # upper growth period
    upperGrowthPeriod = 10

    # gene set
    geneSet = []

    @classmethod  # static method of a class
    def populationName(cls):
        return "Sheep"

    def __init__(self):
        # initialize gene set
        self.gene = Gene()
        # initialize the property value, each property has a base value
        # breeding times for each individual
        self.breedingTimes = 2
        self.age = 8
        self.lifespan = 15
        self.fightCapability = 5
        genderGroup = ["M", "F"]
        self.gender = genderGroup[random.randint(0, 1)]
        self.attackPossibility = 6
        self.defendPossibility = 7
        self.hungryLevel = 5
        self.name = "sheep"

        # add computation for properties based on gene set

    # # forage behaviour of sheep
    def forage(self):
        if self.hungryLevel == 0:
            return False
        else:
            self.hungryLevel -= 1
            return True

    # grow behaviour of a sheep
    def grow(self):
        # If lifespan is over 15, it should die
        if self.age == self.lifespan:
            print("Lifespan is" + self.lifespan + "," + "Now should die :(")
            return False
        # Otherwise it will increase
        self.age += 1
        self.hungryLevel += 1
        if self.lowerGrowthPeriod < self.age < self.upperGrowthPeriod:
            self.defendPossibility += 1
            self.attackPossibility += 1
            self.fightCapability += 1
        elif self.age >= self.upperGrowthPeriod:
            self.defendPossibility -= 1
            self.attackPossibility -= 1
            self.hungryLevel -= 1
            self.fightCapability -= 1

    # attack behaviour of a sheep
    def attack(self, population: Population):
        print("attackPossibility " + str(self.attackPossibility) + " defendPossibility " + str(population.defendPossibility))
        # attackPossibility increase in the growth period
        if self.lowerGrowthPeriod < self.age < self.upperGrowthPeriod:
            self.attackPossibility += 1
        # attack successfully
        if self.attackPossibility > population.defendPossibility:
            print(self.name + " attack" + population.name + " successfully! Fight happened")
            return True
        # attack unsuccessfully, fight not happen
        else:
            return False

    # defend behaviour of a sheep
    def defend(self, population: Population):
        print(" defendPossibility " + str(self.defendPossibility) + " attackPossibility " + str(population.attackPossibility))
        # defendPossibility increase in the growth period
        if self.lowerGrowthPeriod < self.age < self.upperGrowthPeriod:
            self.defendPossibility += 1
        # escape successfully
        if self.defendPossibility > population.attackPossibility:
            print(self.name + " escape successfully! No fight happened")
            return True
        # escape unsuccessfully,fight may happen
        else:
            return False

    # breed behaviour of a sheep
    def breed(self, spouse: Population):
        if self.gender == spouse.gender:
            print("Same gender, no breed")
            return
        if self.breedingTimes > 0:
            if self.lowerGrowthPeriod < self.age < self.upperGrowthPeriod:
                self.breedingTimes -= 1
                self.gene.recombine(spouse.gene)
                return
