#!/usr/bin/python3
import math
import random

from Population import Population
from Gene import Gene


class Wolf(Population):
    """this class defines the properties and behaviours of wolf population"""
    # Gene count for wolf
    __geneCount = 10
    #
    # # lifespan
    # lifespan = None
    #
    # # age
    # age = None
    #
    # # gender
    # gender = None
    #
    # # hungry level
    # hungryLevel = None
    #
    # # attack possibility
    # attackPossibility = None
    #
    # # defend possibility
    # defendPossibility = None
    #
    # # fight capability
    # fightCapability = None
    #
    # # gene set
    # geneSet = []
    #
    # # breeding times for each individual
    # remainingBreedingTimes = 2

    @classmethod  # static method of a class
    def populationName(cls):
        return "Wolf"

    def __init__(self, gene_set=None):
        # initialize gene_set, if no input parameter gene_set or input gene_set is incorrect, randomly generate genes
        if gene_set is None:
            self.gene_set = []
            for j in range(0, Wolf.__geneCount):
                self.gene_set.append(Gene())
        elif len(gene_set) != 10:
            print("Can't create wolf due to incorrect gene_set!")
            self.gene_set = []
            for j in range(0, Wolf.__geneCount):
                self.gene_set.append(Gene())
        else:
            self.gene_set = gene_set

        # static properties initialization
        genderGroup = ["M", "F"]
        self.gender = genderGroup[random.randint(0, 1)]
        self.name = "wolf-" + str(id(self))  # name it with self's address in memory

        # dynamic properties initialization
        self.hungryLevel = 5
        self.age = 0
        self.lifeStatus = "Alive"

        # gene related properties initialization
        self.lifespan = 10  # initialize life with 10, maximum 15 after computation based on gene_set
        self.fightCapability = 50  # initialize fight capability with 50, maximum 100 after computation based on gene_set
        self.attackPossibility = 50  # initialize attack possibility with 50, maximum 100 after computation based on gene_set
        self.defendPossibility = 50  # initialize defend possibility with 50, maximum 100 after computation based on gene_set
        self.remainingBreedingTimes = 1  # initialize remaining breeding times with 1, maximum 3 after computation based on gene_set

        # add computation for properties based on gene set
        # the 1st & 2nd Gene control lifespan, add up all digits from gene (total 2*Gene.__geneLength) with value range [0,1980], then compute the addition to be added to initial value of lifespan
        self.lifespan += math.ceil((self.gene_set[0].sumGeneDigits() + self.gene_set[1].sumGeneDigits()) / 396)
        # the 3rd & 4th Gene control fightCapability, add up all digits from gene (total 2*Gene.__geneLength) with value range [0,1980], then compute the addition to be added to initial value of fightCapability
        self.fightCapability += math.ceil((self.gene_set[2].sumGeneDigits() + self.gene_set[3].sumGeneDigits()) / 39.6)
        # the 5th & 6th Gene control attackPossibility, add up all digits from gene (total 2*Gene.__geneLength) with value range [0,1980], then compute the addition to be added to initial value of attackPossibility
        self.attackPossibility += math.ceil((self.gene_set[4].sumGeneDigits() + self.gene_set[5].sumGeneDigits()) / 39.6)
        # the 7th & 8th Gene control defendPossibility, add up all digits from gene (total 2*Gene.__geneLength) with value range [0,1980], then compute the addition to be added to initial value of defendPossibility
        self.defendPossibility += math.ceil((self.gene_set[6].sumGeneDigits() + self.gene_set[7].sumGeneDigits()) / 39.6)
        # the 9th & 10th Gene control remainingBreedingTimes, add up all digits from gene (total 2*Gene.__geneLength) with value range [0,1980], then compute the addition to be added to initial value of remainingBreedingTimes
        self.remainingBreedingTimes += math.round((self.gene_set[8].sumGeneDigits() + self.gene_set[9].sumGeneDigits()) / 990)

        # lower limit of growth period
        self.lowerGrowthPeriod = math.ceil(self.lifespan / 3)

        # upper limit of growth period
        self.upperGrowthPeriod = 2 * self.lowerGrowthPeriod

    # forage behaviour of wolf
    def forage(self):
        if self.hungryLevel == 0:
            return False
        else:
            self.hungryLevel -= 1
            return True

    # grow behaviour of a wolf
    def grow(self):
        # If age is over lifespan, it should die
        if self.age >= self.lifespan:
            print(self.name + "lifespan is " + str(self.lifespan) + "," + "Now should die :(")
            self.lifeStatus = "Dead"
            return False
        # Otherwise it will increase
        self.age += 1
        if self.hungryLevel < 10:
            self.hungryLevel += 1
        if self.lowerGrowthPeriod < self.age < self.upperGrowthPeriod:
            self.defendPossibility += 1
            self.attackPossibility += 1
            self.fightCapability += 1
        elif self.age >= self.upperGrowthPeriod:
            self.defendPossibility -= 1
            self.attackPossibility -= 1
            self.fightCapability -= 1
            if self.hungryLevel > 1:
                self.hungryLevel -= 1

    # attack behaviour of a wolf
    def attack(self, population: Population):
        print("attackPossibility " + str(self.attackPossibility) + " defendPossibility " + str(
            population.defendPossibility))
        # attackPossibility increase in the growth period
        # if self.lowerGrowthPeriod < self.age < self.upperGrowthPeriod:
        #     self.attackPossibility += 1
        # attack successfully
        if self.attackPossibility > population.defendPossibility:
            print(self.name + " attack" + population.name + " successfully! Fight happened")
            return True
        # attack unsuccessfully, fight not happen
        else:
            return False

    # defend behaviour of a wolf
    def defend(self, population: Population):
        print(" defendPossibility " + str(self.defendPossibility) + " attackPossibility " + str(
            population.attackPossibility))
        # defendPossibility increase in the growth period
        # if self.lowerGrowthPeriod < self.age < self.upperGrowthPeriod:
        #     self.defendPossibility += 1
        # escape successfully
        if self.defendPossibility >= population.attackPossibility:
            print(self.name + " defended successfully!")
            return True
        # defend unsuccessfully
        else:
            return False

    # breed behaviour of a wolf
    def breed(self, spouse):
        if spouse.__class__.__name__ != "Wolf" or self.gender == spouse.gender:
            print("Different population or same gender, no breed")
            return None
        if self.remainingBreedingTimes > 0 and self.lowerGrowthPeriod < self.age < self.upperGrowthPeriod:
            self.remainingBreedingTimes -= 1
            # rebuild gene_set for new baby wolf, get first half gene set from self, another half from spouse
            childGeneSet = []
            # get first half gene set from self after variation
            for i in range(0, int(Wolf.__geneCount/2)):
                childGeneSet.append(self.gene_set[i].variate())
            # get another half gene set from self after variation
            for i in range(int(Wolf.__geneCount/2), Wolf.__geneCount):
                childGeneSet.append(spouse.gene_set[i].variate())
            return Wolf(childGeneSet)
        return None
