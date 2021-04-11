import inspect
import random
import time

from EvolutionSimulation.src.dreamland.Dreamland import Dreamland
from EvolutionSimulation.src.population.Plant import Plant
from EvolutionSimulation.src.population.Population import Population
from EvolutionSimulation.src.tool.CycleInfo import CycleInfo


class PopulationThread:
    """this abstract class defines the common actions of population thread"""

    # # return individual count of a population in the Thread
    # @abstractmethod
    # def getIndividualCount(self): pass

    # update coordinate map after individual's location changing
    def updateDreamLandMap(self, individual: Population, original_slot_code, target_slot_code):
        if original_slot_code is not None:
            self.removeIndividualFromMap(original_slot_code, individual)
        self.appendIndividual2Map(target_slot_code, individual)
        # targetSlotIndividuals = self.dreamland.coordinateMap[target_slot_code]
        # targetSlotIndividuals.append(individual)
        # individual.slotCode = target_slot_code
        # print("self.dreamland.coordinateMap.get(target) is " + str(self.dreamland.coordinateMap.get(target_slot_code)[0].name))

    # move individual location
    def moveLocation(self, individual: Population):
        # possible slots to move to
        targetSlotForSearching = [[1, 0], [2, 0], [0, -1], [0, -2], [-1, 0], [-2, 0], [0, 1], [0, 2]]
        # check if the current slot is near the border of dreamland, remove slots beyond dreamland
        slotNum = individual.slotCode.split("A")
        slotX = int(slotNum[0])
        slotY = int(slotNum[1])
        tmpXGap = int(2 - (Dreamland.SIZE_X - slotX) / 10)
        tmpYGap = int(2 - (Dreamland.SIZE_Y - slotY) / 10)
        while 0 < tmpXGap <= 2:
            targetSlotForSearching.remove([tmpXGap, 0])
            tmpXGap -= 1
        while 0 < tmpYGap <= 2:
            targetSlotForSearching.remove([0, tmpYGap])
            tmpYGap -= 1
        tmpXGap = int(slotX / 10)
        tmpYGap = int(slotY / 10)
        while 0 <= tmpXGap < 2:
            targetSlotForSearching.remove([tmpXGap - 2, 0])
            tmpXGap += 1
        while 0 <= tmpYGap < 2:
            targetSlotForSearching.remove([0, tmpYGap - 2])
            tmpYGap += 1
        # move location randomly
        randDirection = random.randint(0, len(targetSlotForSearching) - 1)
        targetShift = targetSlotForSearching[randDirection]
        targetSlot = Dreamland.computeSlot(individual.slotCode, targetShift[0], targetShift[1])
        if targetSlot is not None:
            individual.coordinateX += targetShift[0] * 10
            individual.coordinateY += targetShift[1] * 10
            self.updateDreamLandMap(individual, individual.slotCode, targetSlot)

    # search food in near 2 slots from 4 directions
    def searchFood(self, individual: Population):
        # near areas to be searched, refer to searching logic
        targetSlotForSearching = [[0, 0], [1, 1], [1, 0], [2, 0], [1, -1], [0, -1], [0, -2], [-1, -1], [-1, 0], [-2, 0], [-1, 1], [0, 1], [0, 2]]
        for targetShift in targetSlotForSearching:
            targetSlot = Dreamland.computeSlot(individual.slotCode, targetShift[0], targetShift[1])
            if targetSlot is not None:
                targetSlotIndividuals = self.dreamland.coordinateMap[targetSlot]
                for food in targetSlotIndividuals:
                    if food.lifeStatus == "Alive":
                        if (individual.populationFeedingType == Population.CARNIVORE and food.populationType == Population.ANIMAL and individual.populationName != food.populationName) or (individual.populationFeedingType == Population.HERBIVORE and food.populationType == Population.PLANT):
                            # self.dreamland.coordinateMap[targetSlot].remove(food)
                            # check target's threat (e.g. wolf won't attach tiger)
                            if individual.populationThreat >= food.populationThreat:
                                return food
        return None

    # search spouse in near 2 slots from 4 directions
    def searchSpouse(self, individual: Population):
        # near areas to be searched, refer to searching logic
        targetSlotForSearching = [[0, 0], [1, 1], [1, 0], [2, 0], [1, -1], [0, -1], [0, -2], [-1, -1], [-1, 0], [-2, 0], [-1, 1], [0, 1], [0, 2]]
        for targetShift in targetSlotForSearching:
            targetSlot = Dreamland.computeSlot(individual.slotCode, targetShift[0], targetShift[1])
            if targetSlot is not None:
                targetSlotIndividuals = self.dreamland.coordinateMap[targetSlot]
                for spouse in targetSlotIndividuals:
                    if spouse.lifeStatus == "Alive":
                        if spouse.populationType == Population.ANIMAL and individual.populationName == spouse.populationName and individual.gender != spouse.gender:
                            return spouse
        return None

    # remove an individual from coordinate map
    def removeIndividualFromMap(self, slotCode, individualForRemove: Population):
        # printStr = "***remove individual(" + individualForRemove.name + "): " + "slotCode(" + str(slotCode) + ") indSlotCode(" + individualForRemove.slotCode + ") indX("
        # printStr += str(individualForRemove.coordinateX) + ") indY("
        # printStr += str(individualForRemove.coordinateY) + ") life("
        # printStr += str(individualForRemove.lifeStatus) + ")    callerModule("
        # printStr += str(inspect.stack()[1][1]) + ")    callerFun("
        # printStr += str(inspect.stack()[1][3]) + ")    callerLine("
        # printStr += str(inspect.stack()[1][2]) + ")"
        # print(printStr)
        # traceback.print_stack()
        self.dreamland.coordinateMap[slotCode].remove(individualForRemove)

    # append an individual to coordinate map
    def appendIndividual2Map(self, slotCode, individualForAppend: Population):
        # printStr = "***append individual(" + individualForAppend.name + "): " + "slotCode(" + str(slotCode) + ") indSlotCode(" + individualForAppend.slotCode + ") indX("
        # printStr += str(individualForAppend.coordinateX) + ") indY("
        # printStr += str(individualForAppend.coordinateY) + ") life("
        # printStr += str(individualForAppend.lifeStatus) + ")"
        # print(printStr)
        self.dreamland.coordinateMap[slotCode].append(individualForAppend)
        individualForAppend.slotCode = slotCode

    # receive cycle info for defending
    def receiveDefendInfo(self, fightResult, pop: Population):
        ownCycles = self.recorder.cycleInfo[self.THREAD_NAME]
        # there is a possibility that upon execution of this method, the iteration in run method hasn't finished yet,
        # so the corresponding cycle info hasn't been saved too wnCycles yet
        while ownCycles.get(self.cycleNumber, None) is None:
            time.sleep(0.01)
        cycle = ownCycles[self.cycleNumber]
        cycle.defendTimes += 1
        pop.fightTimes += 1
        if fightResult == "Success":
            pop.hungryLevel = 0
            cycle.defendSuccessTimes += 1
        elif fightResult == "Failure":
            pop.lifeStatus = "Dead"
            pop.deathCause = "Fight to death"
            pop.deathTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
            cycle.defendFailureTimes += 1
        else:
            pop.hungryLevel += 1
            cycle.defendPeaceTimes += 1

    # add individual to thread
    def addIndividual2Thread(self, pop: Population):
        pop.coordinateX = random.randint(0, Dreamland.SIZE_X)
        pop.coordinateY = random.randint(0, Dreamland.SIZE_Y)
        # set the slot code in the dreamland
        pop.slotCode = Dreamland.returnSlotCode(pop.coordinateX, pop.coordinateY)
        pop.ownThread = self
        self.group.append(pop)
        # update coordinate map
        self.updateDreamLandMap(pop, None, pop.slotCode)

    # monitor all individuals, and execute for all their actions, any thread has different logic, just overwrite this method
    def animalThreadRun(self):
        while self.continueRunning:
            self.num.append(len(self.group))
            print(self.THREAD_NAME + " cycle: " + str(self.cycleNumber + 1) + ".  Remaining individual: " + str(len(self.group)))
            cycleInfo = CycleInfo(self.THREAD_NAME)
            if len(self.group) != 0:
                self.cycleNumber += 1
                for individual in self.group:
                    # check if individual should die naturally
                    if individual.hungryLevel > 10:
                        individual.lifeStatus = "Dead"
                        individual.deathCause = "Starve to death"
                        cycleInfo.newDeathFromStarve += 1
                    elif individual.age >= individual.lifespan:
                        individual.lifeStatus = "Dead"
                        individual.deathCause = "Natural death"
                        cycleInfo.newDeathFromNatural += 1
                    elif individual.deathCause == "Fight to death":
                        cycleInfo.newDeathFromFight += 1
                    # check individual life status first, move to different category if dead (starve to death/natural death/fight to death)
                    if individual.lifeStatus == "Dead":
                        individual.deathTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
                        self.group.remove(individual)
                        self.dead.append(individual)
                        cycleInfo.newDeath += 1
                        continue
                    if not individual.isBusy:
                        individual.isBusy = True
                        # add logic for searching food and fight
                        if individual.hungryLevel > 5:
                            # find food in its own slot, if there is, then fight, if none, change position
                            food = self.searchFood(individual)
                            if food is not None and not food.isBusy:
                                cycleInfo.fightTimes += 1
                                fightResult = individual.fight(food)
                                # if wins, update location to food's location, and remove food from map
                                if fightResult == "Success":
                                    individual.coordinateX = food.coordinateX
                                    individual.coordinateY = food.coordinateY
                                    self.updateDreamLandMap(individual, individual.slotCode, food.slotCode)
                                    self.removeIndividualFromMap(food.slotCode, food)
                                    # self.dreamland.coordinateMap[food.slotCode].remove(food)
                                    cycleInfo.fightSuccessTimes += 1
                                    individual.moveHistory[self.cycleNumber] = str(individual.coordinateX) + "|" + str(individual.coordinateY) + "," + individual.slotCode
                                # if fails, remove individual from map
                                elif fightResult == "Failure":
                                    self.removeIndividualFromMap(individual.slotCode, individual)
                                    # self.dreamland.coordinateMap[individual.slotCode].remove(individual)
                                    cycleInfo.fightFailureTimes += 1
                                elif fightResult == "Flee":
                                    cycleInfo.FleeSuccessTimes += 1
                            # if no food found, move location and become more hungry
                            else:
                                self.moveLocation(individual)
                                individual.hungryLevel += 1
                                individual.moveHistory[self.cycleNumber] = str(individual.coordinateX) + "|" + str(individual.coordinateY) + "," + individual.slotCode
                        # if not hungry enough, prepare for breeding
                        else:
                            # breed logic
                            individual.hungryLevel += 1
                            spouse = self.searchSpouse(individual)
                            if spouse is not None and not spouse.isBusy:
                                cycleInfo.breedTimes += 1
                                child = individual.breed(spouse)
                                if child is not None:
                                    self.addIndividual2Thread(child)
                                    cycleInfo.newBorn += 1
                    individual.isBusy = False
                    individual.age += 1
                    cycleInfo.popAvgHungryLevel += individual.hungryLevel
                    cycleInfo.popAvgAge += individual.age
                    cycleInfo.popAvgLifespan += individual.lifespan
                    cycleInfo.popAvgFightCapability += individual.fightCapability
                    cycleInfo.popAvgAttackPossibility += individual.attackPossibility
                    cycleInfo.popAvgDefendPossibility += individual.defendPossibility
                    cycleInfo.popAvgTotalBreedingTimes += individual.totalBreedingTimes
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
            self.newBronNum.append(cycleInfo.newBorn)
            self.newDeathNum.append(cycleInfo.newDeath)
            self.avgHungryLevel.append(cycleInfo.popAvgHungryLevel)
            self.avgLifespan.append(cycleInfo.popAvgLifespan)
            self.avgFightCapability.append(cycleInfo.popAvgFightCapability)
            self.avgAge.append(cycleInfo.popAvgAge)
            self.avgAttackPossibility.append(cycleInfo.popAvgAttackPossibility)
            self.avgDefendPossibility.append(cycleInfo.popAvgDefendPossibility)
            self.avgTotalBreedingTimes.append(cycleInfo.popAvgTotalBreedingTimes)
            print("cycleInfo.newBorn is " + str(cycleInfo.newBorn))
            print("cycleInfo.newDeath is " + str(cycleInfo.newDeath))

    # plant thread run
    def plantThreadRun(self):
        while self.continueRunning:
            self.num.append(len(self.group))
            print(self.THREAD_NAME + " cycle: " + str(self.cycleNumber + 1) + ".  Remaining individual: " + str(len(self.group)))
            self.cycleNumber += 1
            cycleInfo = CycleInfo(self.THREAD_NAME)
            # generate new plants in each round if plants count is less than 10 times of the slots
            if len(self.group) < int(Dreamland.SIZE_X * Dreamland.SIZE_Y) / 100 * 10:
                for i in range(0, self.cyclePlantCount):
                    # need to randomly initialize the coordinates of the plant
                    plant = Plant()
                    self.addIndividual2Thread(plant)
                cycleInfo.newBorn = self.cyclePlantCount
            if len(self.group) != 0:
                for individual in self.group:
                    # check if individual should die naturally
                    if individual.age >= individual.lifespan:
                        individual.lifeStatus = "Dead"
                        individual.deathCause = "Natural death"
                        cycleInfo.newDeathFromNatural += 1
                    elif individual.deathCause == "Fight to death":
                        cycleInfo.newDeathFromFight += 1
                    # check individual life status first, move to different category if dead (starve to death/natural death/fight to death)
                    if individual.lifeStatus == "Dead":
                        individual.deathTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
                        self.group.remove(individual)
                        self.dead.append(individual)
                        cycleInfo.newDeath += 1
                        continue
                    individual.age += 1
                    cycleInfo.popAvgAge += individual.age
                    cycleInfo.popAvgLifespan += individual.lifespan
                    cycleInfo.popAvgFightCapability += individual.fightCapability
                    cycleInfo.popAvgAttackPossibility += individual.attackPossibility
                    cycleInfo.popAvgDefendPossibility += individual.defendPossibility
            # if there is still live population
            cycleInfo.liveIndividuals = len(self.group)
            cycleInfo.deadIndividuals = len(self.dead)
            if len(self.group) != 0:
                cycleInfo.popAvgAge = round(cycleInfo.popAvgAge / len(self.group), 2)
                cycleInfo.popAvgLifespan = round(cycleInfo.popAvgLifespan / len(self.group), 2)
                cycleInfo.popAvgFightCapability = round(cycleInfo.popAvgFightCapability / len(self.group), 2)
                cycleInfo.popAvgAttackPossibility = round(cycleInfo.popAvgAttackPossibility / len(self.group), 2)
                cycleInfo.popAvgDefendPossibility = round(cycleInfo.popAvgDefendPossibility / len(self.group), 2)
            self.recorder.saveCycleInfo(self.cycleNumber, self, cycleInfo)
            # sleep for 1 day (1s)
            time.sleep(1)
            self.newDeathNum.append(cycleInfo.newDeath)
