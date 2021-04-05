import random
import threading
import time

from EvolutionSimulation.src.population.Population import Population
from EvolutionSimulation.src.thread.PopulationThread import PopulationThread
from EvolutionSimulation.src.tool.CycleInfo import CycleInfo
from EvolutionSimulation.src.tool.Recorder import Recorder
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
    THREAD_NAME = "TigerThread"

    # initialize tiger thread
    def __init__(self, tiger_count, dreamland: Dreamland, recorder: Recorder):
        threading.Thread.__init__(self)
        self.dreamland = dreamland
        self.recorder = recorder
        self.continueRunning = True
        self.initCount = tiger_count
        self.group = []
        self.dead = []
        self.cycleNumber = 0
        for i in range(0, tiger_count):
            # need to randomly initialize the coordinates of the tiger
            tiger = Tiger()
            tiger.coordinateX = random.randint(0, Dreamland.SIZE_X)
            tiger.coordinateY = random.randint(0, Dreamland.SIZE_Y)
            # set the slot code in the dreamland
            tiger.slotCode = Dreamland.returnSlotCode(tiger.coordinateX, tiger.coordinateY)
            tiger.ownThread = self
            tiger.moveHistory[self.cycleNumber] = str(tiger.coordinateX) + "|" + str(tiger.coordinateY) + ", " + tiger.slotCode
            self.group.append(tiger)
            # update coordinate map
            self.updateDreamLandMap(tiger, None, tiger.slotCode)
        # add tiger thread to dreamland
        self.dreamland.populationThreadPlayers.append(self)
        # initialize recorder to record every cycle info
        self.recorder.cycleInfo[TigerThread.THREAD_NAME] = {}

    # monitor all tigers, and execute for all their actions
    def run(self):
        while self.continueRunning:
            print(TigerThread.THREAD_NAME + " cycle: " + str(self.cycleNumber + 1) + ".  Remaining individual: " + str(len(self.group)))
            if len(self.group) != 0:
                self.cycleNumber += 1
                cycleInfo = CycleInfo("Tiger")
                for tiger in self.group:
                    # check if tiger should die naturally
                    if tiger.hungryLevel > 10:
                        tiger.lifeStatus = "Dead"
                        tiger.deathCause = "Starve to death"
                    elif tiger.age >= tiger.lifespan:
                        tiger.lifeStatus = "Dead"
                        tiger.deathCause = "Natural death"
                    # check tiger life status first, move to different category if dead (starve to death/natural death/fight to death)
                    if tiger.lifeStatus == "Dead":
                        tiger.deathTime = time.time()
                        self.group.remove(tiger)
                        self.dead.append(tiger)
                        continue
                    if not tiger.isBusy:
                        tiger.isBusy = True
                        # add logic for searching food and fight
                        if tiger.hungryLevel > 4:
                            # find food in its own slot, if there is, then fight, if none, change position
                            food = self.searchFood(tiger)
                            if food is not None and not food.isBusy:
                                cycleInfo.fightTimes += 1
                                fightResult = tiger.fight(food)
                                # if wins, update location to food's location, and remove food from map
                                if fightResult == "Success":
                                    tiger.coordinateX = food.coordinateX
                                    tiger.coordinateY = food.coordinateY
                                    self.updateDreamLandMap(tiger, tiger.slotCode, food.slotCode)
                                    self.removeIndividual(food.slotCode, food)
                                    # self.dreamland.coordinateMap[food.slotCode].remove(food)
                                    cycleInfo.fightSuccessTimes += 1
                                    tiger.moveHistory[self.cycleNumber] = str(tiger.coordinateX) + "|" + str(tiger.coordinateY) + ", " + tiger.slotCode
                                # if fails, remove tiger from map
                                elif fightResult == "Failure":
                                    self.removeIndividual(tiger.slotCode, tiger)
                                    # self.dreamland.coordinateMap[tiger.slotCode].remove(tiger)
                                    cycleInfo.newDeath += 1
                                    cycleInfo.fightFailureTimes += 1
                                else:
                                    cycleInfo.fightPeaceTimes += 1
                            # if no food found, move location and become more hungry
                            else:
                                self.moveLocation(tiger)
                                tiger.hungryLevel += 1
                                tiger.moveHistory[self.cycleNumber] = str(tiger.coordinateX) + "|" + str(tiger.coordinateY) + ", " + tiger.slotCode
                        # if not hungry enough, prepare for breeding
                        else:
                            # breed logic
                            tiger.hungryLevel += 1
                            spouse = self.searchSpouse(tiger)
                            if spouse is not None and not spouse.isBusy:
                                cycleInfo.breedTimes += 1
                                child = tiger.breed(spouse)
                                if child is not None:
                                    child.coordinateX = random.randint(0, Dreamland.SIZE_X)
                                    child.coordinateY = random.randint(0, Dreamland.SIZE_Y)
                                    # set the slot code in the dreamland
                                    child.slotCode = Dreamland.returnSlotCode(child.coordinateX, child.coordinateY)
                                    self.group.append(child)
                                    # update coordinate map
                                    self.updateDreamLandMap(child, None, child.slotCode)
                                    child.moveHistory[self.cycleNumber] = str(child.coordinateX) + "|" + str(child.coordinateY) + ", " + child.slotCode
                                    cycleInfo.newBorn += 1
                    tiger.isBusy = False
                    tiger.age += 1
                    cycleInfo.popAvgHungryLevel += tiger.hungryLevel
                    cycleInfo.popAvgAge += tiger.age
                    cycleInfo.popAvgLifespan += tiger.lifespan
                    cycleInfo.popAvgFightCapability += tiger.fightCapability
                    cycleInfo.popAvgAttackPossibility += tiger.attackPossibility
                    cycleInfo.popAvgDefendPossibility += tiger.defendPossibility
                    cycleInfo.popAvgTotalBreedingTimes += tiger.TotalBreedingTimes
                # if there is still live population
                cycleInfo.liveIndividuals = len(self.group)
                cycleInfo.deadIndividuals = len(self.dead)
                if len(self.group) != 0:
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
            # if all individuals are dead
            else:
                break