#!/usr/bin/python3
import inspect
import random
import traceback

from EvolutionSimulation.src.dreamland.Dreamland import Dreamland
from EvolutionSimulation.src.population.Population import Population


class PopulationThread:
    """this abstract class defines the common actions of population thread"""

    # # return individual count of a population in the Thread
    # @abstractmethod
    # def getIndividualCount(self): pass

    # update coordinate map after individual's location changing
    def updateDreamLandMap(self, individual: Population, original_slot_code, target_slot_code):
        if original_slot_code is not None:
            self.removeIndividual(original_slot_code, individual)
        self.appendIndividual(target_slot_code, individual)
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
    def removeIndividual(self, slotCode, individualForRemove):
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
    def appendIndividual(self, slotCode, individualForAppend):
        # printStr = "***append individual(" + individualForAppend.name + "): " + "slotCode(" + str(slotCode) + ") indSlotCode(" + individualForAppend.slotCode + ") indX("
        # printStr += str(individualForAppend.coordinateX) + ") indY("
        # printStr += str(individualForAppend.coordinateY) + ") life("
        # printStr += str(individualForAppend.lifeStatus) + ")"
        # print(printStr)
        self.dreamland.coordinateMap[slotCode].append(individualForAppend)
        individualForAppend.slotCode = slotCode