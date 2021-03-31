#!/usr/bin/python3
from abc import ABCMeta, abstractmethod
from random import random

import Dreamland
from EvolutionSimulation.src.Population import Population


class PopulationThread:
    """this abstract class defines the common actions of population thread"""

    # # return individual count of a population in the Thread
    # @abstractmethod
    # def getIndividualCount(self): pass

    # update coordinate map after individual's location changing
    def updateDreamLandMap(self, individual: Population, original, target):
        targetSlotIndividuals = []
        if original is not None:
            originalSlotIndividuals = self.dreamland.coordinateMap[original]
            originalSlotIndividuals.remove(individual)
        targetSlotIndividuals = self.dreamland.coordinateMap[target]
        targetSlotIndividuals.append(individual)
        print("self.dreamland.coordinateMap.get(target) is " + str(self.dreamland.coordinateMap.get(target)[0].name))
        print("target is " + str(target))
        print("dreamland is " + str(self.dreamland))

    # move individual location
    def moveLocation(self, individual: Population):
        moveDirection = random.randint(1, 4)
        originalSlot = individual.slotCode
        # move east
        if moveDirection == 1:
            individual.coordinateX += 10
            if individual.coordinateX > Dreamland.SIZE_X:
                individual.coordinateX = Dreamland.SIZE_X
        # move south
        elif moveDirection == 2:
            individual.coordinateY -= 10
            if individual.coordinateY < 0:
                individual.coordinateY = 0
        # move west
        elif moveDirection == 3:
            individual.coordinateX -= 10
            if individual.coordinateX < 0:
                individual.coordinateX = 0
        # move north
        else:
            individual.coordinateY += 10
            if individual.coordinateY > Dreamland.SIZE_Y:
                individual.coordinateY = Dreamland.SIZE_Y
        individual.slotCode = Dreamland.returnSlotNo(individual.coordinateX, individual.coordinateY)
        self.updateDreamLandMap(individual, originalSlot, individual.slotCode)

    # search food in near 2 slots from 4 directions
    def searchFood(self, individual: Population):
        # near areas to be searched, refer to searching logic
        targetSlotForSearching = [[1, 1], [1, 0], [2, 0], [1, -1], [0, -1], [0, -2], [-1, -1], [-1, 0], [-2, 0], [-1, 1], [0, 1], [0, 2]]
        for targetShift in targetSlotForSearching:
            targetSlot = Dreamland.computeSlot(individual.slotCode, targetShift[0], targetShift[1])
            if targetSlot is not None:
                targetSlotIndividuals = self.dreamland.coordinateMap[targetSlot]
                for food in targetSlotIndividuals:
                    if (individual.populationFeedingType == Population.CARNIVORE and food.populationType == Population.ANIMAL) or (individual.populationFeedingType == Population.HERBIVORE and food.populationType == Population.PLANT):
                        return food
        return None
