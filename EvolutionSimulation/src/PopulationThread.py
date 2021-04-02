#!/usr/bin/python3
from abc import ABCMeta, abstractmethod
from random import random

from Dreamland import Dreamland
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

    # move individual location
    def moveLocation(self, individual: Population):
        # possible slots to move to
        targetSlotForSearching = [[1, 0], [2, 0], [0, -1], [0, -2], [-1, 0], [-2, 0], [0, 1], [0, 2]]
        # check if the current slot is near the border of dreamland
        slotNum = individual.slotCode.split("A")
        slotX = int(slotNum[0])
        slotY = int(slotNum[1])
        if Dreamland.SIZE_X - slotX == 0:
            targetSlotForSearching.remove([1, 0])
            targetSlotForSearching.remove([2, 0])
        elif Dreamland.SIZE_X - slotX == 10:
            targetSlotForSearching.remove([2, 0])
        if Dreamland.SIZE_Y - slotY == 0:
            targetSlotForSearching.remove([0, 1])
            targetSlotForSearching.remove([0, 2])
        elif Dreamland.SIZE_Y - slotY == 10:
            targetSlotForSearching.remove([0, 2])
        if slotX == 0:
            targetSlotForSearching.remove([-1, 0])
            targetSlotForSearching.remove([-2, 0])
        elif slotX == 10:
            targetSlotForSearching.remove([-2, 0])
        if slotY == 0:
            targetSlotForSearching.remove([0, -1])
            targetSlotForSearching.remove([0, -2])
        elif slotY == 10:
            targetSlotForSearching.remove([0, -2])
        randDirection = random.randint(0, len(targetSlotForSearching) - 1)
        targetShift = targetSlotForSearching[randDirection]
        targetSlot = Dreamland.computeSlot(individual.slotCode, targetShift[0], targetShift[1])
        if targetSlot is not None:
            individual.coordinateX += targetShift[0] * 10
            individual.coordinateY += targetShift[1] * 10
            self.updateDreamLandMap(individual, individual.slotCode, targetSlot)
            individual.slotCode = targetSlot

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
                        self.dreamland.coordinateMap[targetSlot].remove(food)
                        return food
        return None

    def searchSpouse(self, individual: Population):
        # near areas to be searched, refer to searching logic
        targetSlotForSearching = [[1, 1], [1, 0], [2, 0], [1, -1], [0, -1], [0, -2], [-1, -1], [-1, 0], [-2, 0], [-1, 1], [0, 1], [0, 2]]
        for targetShift in targetSlotForSearching:
            targetSlot = Dreamland.computeSlot(individual.slotCode, targetShift[0], targetShift[1])
            if targetSlot is not None:
                targetSlotIndividuals = self.dreamland.coordinateMap[targetSlot]
                for spouse in targetSlotIndividuals:
                    if spouse.populationType == Population.ANIMAL and individual.name.split("-")[0] == spouse.name.split("-")[0] and individual.gender != spouse.gender:
                        return spouse
        return None
