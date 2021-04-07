import time

from EvolutionSimulation.src.population.Population import Population


class Plant(Population):
    """this class defines the properties and behaviours of plant population"""

    populationName = "Plant"

    def __init__(self):
        self.name = "plant-" + str(id(self))  # name it with self's address in memory
        self.birthTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.deathTime = None  # to be writen upon death
        self.deathCause = None  # to be write upon death
        self.populationType = Population.PLANT
        self.populationThreat = 0   # this property is visible to other population, if own value is bigger than other population, then attack; otherwise, don't attack

        # dynamic properties initialization
        self.age = 0
        self.lifeStatus = "Alive"
        self.coordinateX = 0
        self.coordinateY = 0
        self.slotCode = ""
        self.isBusy = False
        self.fightTimes = 0
        self.ownThread = None

        # gene related properties initialization
        self.lifespan = 20
        self.fightCapability = 0
        self.attackPossibility = 0
        self.defendPossibility = 0