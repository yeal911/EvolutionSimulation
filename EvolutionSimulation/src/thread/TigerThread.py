import random
import threading
import time

from PopulationThread import PopulationThread
from EvolutionSimulation.src.dreamland.Dreamland import Dreamland
from EvolutionSimulation.src.population.Tiger import Tiger


class TigerThread(threading.Thread, PopulationThread):
    """
    Thread for tiger population, to evolute all the individuals of tiger population

    ***parameter explanation***
    dreamland: where this thread runs
    initCount: initiate the tiger count to be loaded to dream land
    coordinateX: x coordinate in dream land
    coordinateY: y coordinate in dream land
    slotCode: slot code computed
    group: all the individuals
    dead: all dead individuals
    """

    # initialize tiger thread
    def __init__(self, tiger_count, dreamland: Dreamland):
        threading.Thread.__init__(self)
        self.dreamland = dreamland
        self.initCount = tiger_count
        self.group = []
        self.dead = []
        for i in range(0, tiger_count):
            # need to randomly initialize the coordinates of the tiger
            tiger = Tiger()
            tiger.coordinateX = random.randint(0, Dreamland.SIZE_X)
            tiger.coordinateY = random.randint(0, Dreamland.SIZE_Y)
            # set the slot code in the dreamland
            tiger.slotCode = Dreamland.returnSlotCode(tiger.coordinateX, tiger.coordinateY)
            self.group.append(tiger)
            # update coordinate map
            self.updateDreamLandMap(tiger, None, tiger.slotCode)
        # add tiger thread to dreamland
        self.dreamland.populationThreadPlayers.append(self)

    # monitor all wolves, and execute for all their actions
    def run(self):
        while True:
            for tiger in self.group:
                # check if tiger should die naturally
                if tiger.hungryLevel > 10 or tiger.age >= tiger.lifespan:
                    tiger.lifeStatus = "Dead"
                    tiger.deathTime = time.time()
                # check tiger life status first, move to different category if dead (starve to death/natural death/fight to death)
                if tiger.lifeStatus == "Dead":
                    self.group.remove(tiger)
                    self.dead.append(tiger)
                    continue
                if not tiger.isBusy:
                    tiger.isBusy = True
                    # add logic for searching food and fight
                    if tiger.hungryLevel > 4:
                        # find food in its own slot, if there is, then flight, if none, change position
                        food = PopulationThread.searchFood(tiger)
                        if food is not None:
                            fightResult = tiger.fight(food)
                            # if wins, update location to food's location, and remove food from map
                            if fightResult == "Success":
                                self.updateDreamLandMap(tiger, tiger.slotCode, food.slotCode)
                                self.dreamland.coordinateMap[food.slotCode].remove(food)
                            # if fails, remove tiger from map
                            elif fightResult == "Failure":
                                self.dreamland.coordinateMap[tiger.slotCode].remove(tiger)
                        # if no food found, move location and become more hungry
                        else:
                            PopulationThread.moveLocation(tiger)
                            tiger.hungryLevel += 1
                    # if not hungry enough, prepare for breeding
                    else:
                        # breed logic
                        spouse = PopulationThread.searchSpouse(tiger)
                        if spouse is not None:
                            child = tiger.breed(spouse)
                            if child is not None:
                                child.coordinateX = random.randint(0, Dreamland.SIZE_X)
                                child.coordinateY = random.randint(0, Dreamland.SIZE_Y)
                                # set the slot code in the dreamland
                                child.slotCode = Dreamland.returnSlotCode(child.coordinateX, child.coordinateY)
                                self.group.append(child)
                                # update coordinate map
                                self.updateDreamLandMap(child, None, child.slotCode)
                        else:
                            tiger.hungryLevel += 1
                tiger.isBusy = False
                tiger.age += 1
            # sleep for 1 day (1s)
            time.sleep(1)