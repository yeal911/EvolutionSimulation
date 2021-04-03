import random
import threading
import time

from PopulationThread import PopulationThread
from EvolutionSimulation.src.dreamland.Dreamland import Dreamland
from EvolutionSimulation.src.population.Wolf import Wolf


class WolfThread(threading.Thread, PopulationThread):
    """
    Thread for wolf population, to evolute all the individuals of wolf population

    ***parameter explanation***
    dreamland: where this thread runs
    initCount: initiate the wolf count to be loaded to dream land
    coordinateX: x coordinate in dream land
    coordinateY: y coordinate in dream land
    slotCode: slot code computed
    group: all the individuals
    dead: all dead individuals
    """

    # initialize wolf thread
    def __init__(self, wolf_count, dreamland: Dreamland):
        threading.Thread.__init__(self)
        self.dreamland = dreamland
        self.initCount = wolf_count
        self.group = []
        self.dead = []
        for i in range(0, wolf_count):
            # need to randomly initialize the coordinates of the wolf
            wolf = Wolf()
            wolf.coordinateX = random.randint(0, Dreamland.SIZE_X)
            wolf.coordinateY = random.randint(0, Dreamland.SIZE_Y)
            # set the slot code in the dreamland
            wolf.slotCode = Dreamland.returnSlotCode(wolf.coordinateX, wolf.coordinateY)
            self.group.append(wolf)
            # update coordinate map
            self.updateDreamLandMap(wolf, None, wolf.slotCode)
        # add wolf thread to dreamland
        self.dreamland.populationThreadPlayers.append(self)

    # monitor all wolves, and execute for all their actions
    def run(self):
        while True:
            # sleep for 1 day (1s)
            time.sleep(1)
            for wolf in self.wolves:
                # add logic for forage, find for food if it is hungry
                if wolf.hungryLevel > 5:
                    # find food in its own slot, if there is, then flight, if none, change position
                    print(wolf.name + " hungryLevel: " + str(wolf.hungryLevel))
                else:
                    print(wolf.name + " hungryLevel: " + str(wolf.hungryLevel))
                # add logic for grow

                # add logic for flight

                # add logic for breed

