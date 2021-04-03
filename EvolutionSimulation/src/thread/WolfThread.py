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
            for wolf in self.group:
                # check if wolf should die naturally
                if wolf.hungryLevel > 10 or wolf.age >= wolf.lifespan:
                    wolf.lifeStatus = "Dead"
                    wolf.deathTime = time.time()
                # check wolf life status first, move to different category if dead (starve to death/natural death/fight to death)
                if wolf.lifeStatus == "Dead":
                    self.group.remove(wolf)
                    self.dead.append(wolf)
                    continue
                if not wolf.isBusy:
                    wolf.isBusy = True
                    # add logic for searching food and fight
                    if wolf.hungryLevel > 4:
                        # find food in its own slot, if there is, then flight, if none, change position
                        food = PopulationThread.searchFood(wolf)
                        if food is not None:
                            fightResult = wolf.fight(food)
                            # if wins, update location to food's location, and remove food from map
                            if fightResult == "Success":
                                self.updateDreamLandMap(wolf, wolf.slotCode, food.slotCode)
                                self.dreamland.coordinateMap[food.slotCode].remove(food)
                            # if fails, remove wolf from map
                            elif fightResult == "Failure":
                                self.dreamland.coordinateMap[wolf.slotCode].remove(wolf)
                        # if no food found, move location and become more hungry
                        else:
                            PopulationThread.moveLocation(wolf)
                            wolf.hungryLevel += 1
                    # if not hungry enough, prepare for breeding
                    else:
                        # breed logic
                        spouse = PopulationThread.searchSpouse(wolf)
                        if spouse is not None:
                            child = wolf.breed(spouse)
                            if child is not None:
                                child.coordinateX = random.randint(0, Dreamland.SIZE_X)
                                child.coordinateY = random.randint(0, Dreamland.SIZE_Y)
                                # set the slot code in the dreamland
                                child.slotCode = Dreamland.returnSlotCode(child.coordinateX, child.coordinateY)
                                self.group.append(child)
                                # update coordinate map
                                self.updateDreamLandMap(child, None, child.slotCode)
                        else:
                            wolf.hungryLevel += 1
                wolf.isBusy = False
                wolf.age += 1
            # sleep for 1 day (1s)
            time.sleep(1)