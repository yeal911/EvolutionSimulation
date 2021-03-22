#!/usr/bin/python3
import random

from Population import Population
from Gene import Gene


class Sheep(Population):
    """this class defines the properties and behaviours of sheep population"""

    @classmethod  # static method of a class
    def populationName(cls):
        return "Sheep"

    def __init__(self, gene=None):
        # initialize gene set
        if gene is None:
            self.gene = Gene()
        else:
            self.gene = gene

        # breeding times for each individual
        self.breedingTimes = 2
        self.age = 0
        self.fightCapability = 5
        self.name = "sheep"

        # add computation for properties based on gene set

        # lifespan in 2 times first 2 digits of gene
        self.lifespan = 2 * (self.gene.geneDigits[0] + self.gene.geneDigits[1])

        # gender
        if self.gene.geneDigits[2] % 2 == 0:
            self.gender = "M"
        else:
            self.gender = "F"

        # attackPossibility
        self.attackPossibility = self.gene.geneDigits[3]

        # defendPossibility
        self.defendPossibility = self.gene.geneDigits[4]

        # hungryLevel
        self.hungryLevel = (self.gene.geneDigits[5] + self.gene.geneDigits[6]) / 2

        # lower limit of growth period
        # self.lowerGrowthPeriod = self.lifespan / 3
        self.lowerGrowthPeriod = self.lifespan / 3

        # upper limit of growth period
        self.upperGrowthPeriod = 2 * self.lowerGrowthPeriod

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
            print("Lifespan is " + str(self.lifespan) + "," + "Now should die :(")
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
        print("attackPossibility " + str(self.attackPossibility) + " defendPossibility " + str(
            population.defendPossibility))
        # attackPossibility increase in the growth period
        if self.lowerGrowthPeriod < self.age < self.upperGrowthPeriod:
            self.attackPossibility += 1
        # attack successfully
        if self.attackPossibility > population.defendPossibility:
            print(self.name + " attack" + population.name + " successfully! Fight happened")
            if self.attackPossibility - population.defendPossibility > 2:
                self.attackPossibility += 1
                population.attackPossibility -= 1
            else:
                population.defendPossibility += 1
                self.attackPossibility -= 1
            return True
        # attack unsuccessfully, fight not happen
        else:
            return False

    # defend behaviour of a sheep
    def defend(self, population: Population):
        print(" defendPossibility " + str(self.defendPossibility) + " attackPossibility " + str(
            population.attackPossibility))
        # defendPossibility increase in the growth period
        if self.lowerGrowthPeriod < self.age < self.upperGrowthPeriod:
            self.defendPossibility += 1
        # escape successfully
        if self.defendPossibility > population.attackPossibility:
            print(self.name + " escape successfully! No fight happened")
            return True
        # escape unsuccessfully,fight may happen
        else:
            if population.attackPossibility - self.defendPossibility > 2:
                self.attackPossibility -= 1
                population.attackPossibility += 1
            else:
                population.defendPossibility -= 1
                self.attackPossibility += 1
            return False

    # breed behaviour of a sheep
    def breed(self, spouse: Population):
        if self.gender == spouse.gender:
            print("Same gender, no breed")
            return
        if self.breedingTimes > 0:
            if self.lowerGrowthPeriod < self.age < self.upperGrowthPeriod:
                self.breedingTimes -= 1
                gene = self.gene.recombine(spouse.gene)
                print("Father is " + str(self.gene.geneDigits) + " Mother is " + str(spouse.gene.geneDigits))
                new_sheep = Sheep(gene)
                return new_sheep

    # set gene
    def set_gene(self, gene: Gene):
        self.gene = gene