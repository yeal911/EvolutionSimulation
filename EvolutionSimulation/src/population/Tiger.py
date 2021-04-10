import math
import random
import time

from EvolutionSimulation.src.gene.Gene import Gene
from EvolutionSimulation.src.population.Population import Population


class Tiger(Population):
    """this class defines the properties and behaviours of tiger population"""

    populationName = "Tiger"

    def __init__(self, gene=None, generation=1, parents=""):
        # initialize gene_set, if no input parameter gene_set or input gene_set is incorrect, randomly generate genes
        if gene is None:
            self.gene = Gene()
        else:
            self.gene = gene
        # static properties initialization
        genderGroup = ["M", "F"]
        self.gender = genderGroup[random.randint(0, 1)]
        self.name = "tiger-" + str(id(self))  # name it with self's address in memory
        self.generation = generation
        self.parents = parents
        self.birthTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.deathTime = None  # to be writen upon death
        self.deathCause = None  # to be write upon death
        self.populationFeedingType = Population.CARNIVORE
        self.populationType = Population.ANIMAL
        self.populationThreat = 8   # this property is visible to other population, if own value is bigger than other population, then attack; otherwise, don't attack

        # dynamic properties initialization
        self.hungryLevel = 1  # maximum hungry level is 10, population will die if beyond 10
        self.age = 0
        self.lifeStatus = "Alive"
        self.coordinateX = 0
        self.coordinateY = 0
        self.slotCode = ""
        self.isBusy = False
        self.fightTimes = 0
        self.breedTimes = 0
        self.ownThread = None

        # for debug purpose, key is cycle number, value is location
        self.moveHistory = {}

        # gene related properties initialization
        self.lifespan = 10  # initialize life with 10, maximum 15 after computation based on gene_set
        self.fightCapability = 70  # initialize fight capability with 50, maximum 100 after computation based on gene_set
        self.attackPossibility = 70  # initialize attack possibility with 50, maximum 100 after computation based on gene_set
        self.defendPossibility = 70  # initialize defend possibility with 50, maximum 100 after computation based on gene_set
        self.totalBreedingTimes = 1  # initialize remaining breeding times with 1, maximum 2 after computation based on gene_set

        # the 1st bit of Gene controls lifespan
        # then compute the addition to be added to initial value of lifespan
        self.lifespan += math.ceil(self.gene.geneDigits[0] / 20)
        # the 2nd bit of Gene controls fightCapability
        # then compute the addition to be added to initial value of fightCapability
        self.fightCapability += math.ceil(self.gene.geneDigits[1] / 3.3)
        # the 3rd bit of Gene controls attackPossibility
        # then compute the addition to be added to initial value of attackPossibility
        self.attackPossibility += math.ceil(self.gene.geneDigits[2] / 3.3)
        # the 4th bit of Gene controls defendPossibility
        # then compute the addition to be added to initial value of defendPossibility
        self.defendPossibility += math.ceil(self.gene.geneDigits[3] / 3.3)
        # the 5th bit of Gene controls totalBreedingTimes
        # then compute the addition to be added to initial value of totalBreedingTimes
        self.totalBreedingTimes += round(self.gene.geneDigits[4] / 50)

        # lower limit of growth period
        self.lowerGrowthPeriod = math.ceil(self.lifespan / 3)
        # upper limit of growth period
        self.upperGrowthPeriod = 2 * self.lowerGrowthPeriod

    # new child born
    @staticmethod
    def newChild(gene: Gene, generation, parents):
        return Tiger(gene, generation, parents)