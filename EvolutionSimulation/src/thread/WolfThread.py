import random
import threading
import time

from EvolutionSimulation.src.thread.PopulationThread import PopulationThread
from EvolutionSimulation.src.tool.CycleInfo import CycleInfo
from EvolutionSimulation.src.tool.Recorder import Recorder
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
    THREAD_NAME = "WolfThread"

    # initialize wolf thread
    def __init__(self, wolf_count, dreamland: Dreamland, recorder: Recorder):
        threading.Thread.__init__(self)
        self.dreamland = dreamland
        self.recorder = recorder
        self.initCount = wolf_count
        self.group = []
        self.dead = []
        self.cycleNumber = 0
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
        # initialize recorder to record every cycle info
        self.recorder.cycleInfo[WolfThread.THREAD_NAME] = {}

    # monitor all wolves, and execute for all their actions
    def run(self):
        while True:
            self.cycleNumber += 1
            cycleInfo = CycleInfo("Wolf")
            for wolf in self.group:
                # check if wolf should die naturally
                if wolf.hungryLevel > 10:
                    wolf.lifeStatus = "Dead"
                    wolf.deathCause = "Starve to death"
                elif wolf.age >= wolf.lifespan:
                    wolf.lifeStatus = "Dead"
                    wolf.deathCause = "Natural death"
                # check wolf life status first, move to different category if dead (starve to death/natural death/fight to death)
                if wolf.lifeStatus == "Dead":
                    wolf.deathTime = time.time()
                    self.group.remove(wolf)
                    self.dead.append(wolf)
                    continue
                if not wolf.isBusy:
                    wolf.isBusy = True
                    # add logic for searching food and fight
                    if wolf.hungryLevel > 4:
                        # find food in its own slot, if there is, then flight, if none, change position
                        food = self.searchFood(wolf)
                        if food is not None:
                            cycleInfo.fightTimes += 1
                            fightResult = wolf.fight(food)
                            # if wins, update location to food's location, and remove food from map
                            if fightResult == "Success":
                                self.updateDreamLandMap(wolf, wolf.slotCode, food.slotCode)
                                self.dreamland.coordinateMap[food.slotCode].remove(food)
                                cycleInfo.fightSuccessTimes += 1
                            # if fails, remove wolf from map
                            elif fightResult == "Failure":
                                self.dreamland.coordinateMap[wolf.slotCode].remove(wolf)
                                cycleInfo.newDeath += 1
                                cycleInfo.fightFailureTimes += 1
                            else:
                                cycleInfo.fightPeaceTimes += 1
                        # if no food found, move location and become more hungry
                        else:
                            self.moveLocation(wolf)
                            wolf.hungryLevel += 1
                    # if not hungry enough, prepare for breeding
                    else:
                        # breed logic
                        spouse = self.searchSpouse(wolf)
                        if spouse is not None:
                            cycleInfo.breedTimes += 1
                            child = wolf.breed(spouse)
                            if child is not None:
                                child.coordinateX = random.randint(0, Dreamland.SIZE_X)
                                child.coordinateY = random.randint(0, Dreamland.SIZE_Y)
                                # set the slot code in the dreamland
                                child.slotCode = Dreamland.returnSlotCode(child.coordinateX, child.coordinateY)
                                self.group.append(child)
                                # update coordinate map
                                self.updateDreamLandMap(child, None, child.slotCode)
                                cycleInfo.newBorn += 1
                        else:
                            wolf.hungryLevel += 1
                wolf.isBusy = False
                wolf.age += 1
                cycleInfo.popAvgHungryLevel += wolf.hungryLevel
                cycleInfo.popAvgAge += wolf.age
                cycleInfo.popAvgLifespan += wolf.lifespan
                cycleInfo.popAvgFightCapability += wolf.fightCapability
                cycleInfo.popAvgAttackPossibility += wolf.attackPossibility
                cycleInfo.popAvgDefendPossibility += wolf.defendPossibility
                cycleInfo.popAvgTotalBreedingTimes += wolf.TotalBreedingTimes
            # if there is still live population
            if len(self.group) != 0:
                cycleInfo.liveIndividuals = len(self.group)
                cycleInfo.deadIndividuals = len(self.dead)
                cycleInfo.popAvgHungryLevel = round(cycleInfo.popAvgHungryLevel / len(self.group), 2)
                cycleInfo.popAvgAge = round(cycleInfo.popAvgAge / len(self.group), 2)
                cycleInfo.popAvgLifespan = round(cycleInfo.popAvgLifespan / len(self.group), 2)
                cycleInfo.popAvgFightCapability = round(cycleInfo.popAvgFightCapability / len(self.group), 2)
                cycleInfo.popAvgAttackPossibility = round(cycleInfo.popAvgAttackPossibility / len(self.group), 2)
                cycleInfo.popAvgDefendPossibility = round(cycleInfo.popAvgDefendPossibility / len(self.group), 2)
                cycleInfo.popAvgTotalBreedingTimes = round(cycleInfo.popAvgTotalBreedingTimes / len(self.group), 2)
                self.recorder.saveCycleInfo(self.cycleNumber, self, cycleInfo)
                # sleep for 1 day (1s)
                time.sleep(1)
            # if all of this population are dead, sleep this thread
            else:
                time.sleep(5)