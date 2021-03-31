#!/usr/bin/python3
import math
import random
import time

from Population import Population
from Gene import Gene


class Sheep(Population):
    """this class defines the properties and behaviours of sheep population"""

    @classmethod  # static method of a class
    def populationName(cls):
        return "Sheep"

    def __init__(self, gene=None, generation=1):
        # initialize gene set
        if gene is None:
            self.gene = Gene()
        else:
            self.gene = gene

        self.fightCapability = 5
        self.name = "sheep-" + str(id(self))  # name it with self's address in memory

        self.generation = generation
        self.birthTime = time.time()
        self.deathTime = None  # to be writen upon death
        self.populationFeedingType = Population.CARNIVORE
        self.populationType = Population.ANIMAL

        # dynamic properties initialization
        self.hungryLevel = 5
        self.age = 0
        self.lifeStatus = "Alive"
        self.coordinateX = 0
        self.coordinateY = 0
        self.slotCode = ""

        # gene related properties initialization
        self.lifespan = 13  # initialize life with 10, maximum 15 after computation based on gene_set
        self.fightCapability = 45  # initialize fight capability with 50, maximum 100 after computation based on gene_set
        self.attackPossibility = 50  # initialize attack possibility with 50, maximum 100 after computation based on gene_set
        self.defendPossibility = 50  # initialize defend possibility with 50, maximum 100 after computation based on gene_set
        self.remainingBreedingTimes = 5  # initialize remaining breeding times with 1, maximum 3 after computation based on gene_set

        # lifespan in 2 times first 2 digits of gene
        self.lifespan += math.ceil(self.gene.geneDigits[0] / 20)
        # gender
        if self.gene.geneDigits[2] % 2 == 0:
            self.gender = "M"
        else:
            self.gender = "F"
        genderGroup = ["M", "F"]
        self.gender = genderGroup[random.randint(0, 1)]
        # attackPossibility
        self.attackPossibility = self.gene.geneDigits[3]

        # defendPossibility
        self.defendPossibility = self.gene.geneDigits[4]

        # fightPossibility
        self.fightCapability = min(60, self.gene.geneDigits[7])

        # hungryLevel
        # self.hungryLevel = (self.gene.geneDigits[5] + self.gene.geneDigits[6]) / 2
        self.hungryLevel = 5
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
        if self.age >= self.lifespan:
            print("Lifespan is " + str(self.lifespan) + "," + "Now should die :(")
            self.lifeStatus = "Dead"
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
    # def attack(self, population: Population):
    #     print("fightCapability " + str(self.fightCapability) + " fightCapability " + str(
    #         population.fightCapability))
    #     # attackPossibility increase in the growth period
    #     if self.lowerGrowthPeriod < self.age < self.upperGrowthPeriod:
    #         self.fightCapability += 1
    #     # attack successfully
    #     if self.fightCapability > population.fightCapability:
    #         print(self.name + " attack" + population.name + " successfully! Fight happened")
    #         if self.fightCapability - population.fightCapability > 2:
    #             self.fightCapability += 1
    #             population.fightCapability -= 1
    #         else:
    #             population.fightCapability += 1
    #             self.fightCapability -= 1
    #         return True
    #     # attack unsuccessfully, fight not happen
    #     else:
    #         return False
    #
    # # defend behaviour of a sheep
    # def defend(self, population: Population):
    #     print(" fightCapability " + str(self.fightCapability) + " fightCapability " + str(
    #         population.fightCapability))
    #     # defendPossibility increase in the growth period
    #     if self.lowerGrowthPeriod < self.age < self.upperGrowthPeriod:
    #         self.fightCapability += 1
    #     # escape successfully
    #     if self.fightCapability > population.fightCapability:
    #         print(self.name + " escape successfully! No fight happened")
    #         return True
    #     # escape unsuccessfully,fight may happen
    #     else:
    #         if population.fightCapability - self.fightCapability > 2:
    #             self.fightCapability -= 1
    #             population.fightCapability += 1
    #         else:
    #             population.fightCapability -= 1
    #             self.fightCapability += 1
    #         return False

    def fight(self, population: Population):
        if self.fightCapability > population.fightCapability:
            if self.lowerGrowthPeriod < self.age < self.upperGrowthPeriod:
                self.fightCapability += 1
                return "Success"
        elif self.fightCapability == population.fightCapability:
            return "Peace"
        else:
            self.lifeStatus = "Dead"
            return "Failure"

    # breed behaviour of a sheep
    def breed(self, spouse: Population):
        if self.gender == spouse.gender:
            print("Same gender, no breed")
            return
        if self.remainingBreedingTimes > 0:
            if self.lowerGrowthPeriod < self.age < self.upperGrowthPeriod:
                self.remainingBreedingTimes -= 1
                gene = self.gene.recombine(spouse.gene)
                print("Father is " + str(self.gene.geneDigits) + " Mother is " + str(spouse.gene.geneDigits))
                new_sheep = Sheep(gene)
                return new_sheep

    # set gene
    def set_gene(self, gene: Gene):
        self.gene = gene
