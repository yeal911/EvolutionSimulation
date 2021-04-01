#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt

from EvolutionSimulation.src import PopulationThread


class Dreamland:
    """
    the playground of all populations, with X & Y coordinates.
    The whole dreamland will be divided to different slots per 10 scale.
    The slots are coded with codes like 1010/1020/2010 etc.
    1010 means the rectangle area from [0,0] to (10,10) in the coordinate axis.

    ***parameter explanation***
    populationThreadPlayers: stores all the Population Threads which should be added in Thread's own structure method
    coordinateMap: it is a dict, it has all the land slot no.s as the key, and the value is population individuals which are added/removed from Thread's logic
    """
    SIZE_X = 100
    SIZE_Y = 100

    def __init__(self):
        # all population thread players
        self.populationThreadPlayers = []
        # coordinate map(dict) for searching, key is slot no., value is population individuals.
        self.coordinateMap = {}
        # initialize coordinate map
        for i in range(10, Dreamland.SIZE_X + 1, 10):
            for j in range(10, Dreamland.SIZE_Y + 1, 10):
                mapKey = str(i) + "A" + str(j)
                self.coordinateMap[mapKey] = []

    # add population player into this dreamland
    def addPopulationPlayer(self, pt: PopulationThread):
        self.populationThreadPlayers.append(pt)
        pt.start()

    # remove population player from this dreamland
    def removePopulationPlayer(self, pt: PopulationThread):
        self.populationThreadPlayers.remove(pt)
        # stop running thread
        pt.join()

    # start population threar
    def startPopulationThread(self, pt: PopulationThread):
        pt.start()

    # return slot no. with input x and y coordinates
    @staticmethod
    def returnSlotNo(x, y):
        codeX = (x//10 + 1) * 10
        codeY = (y//10 + 1) * 10
        return str(codeX) + "A" + str(codeY)

    # compute slot code after movement, check whether the target slot still inside the dreamland, if no then return None, otherwise return target slot code
    @staticmethod
    def computeSlot(slot_code, x_slot_shift, y_slot_shift):
        slotNum = slot_code.split("A")
        targetSlotX = int(slotNum[0]) + x_slot_shift * 10
        targetSlotY = int(slotNum[1]) + y_slot_shift * 10
        if targetSlotX > Dreamland.SIZE_X or targetSlotY > Dreamland.SIZE_Y or targetSlotX < 10 or targetSlotY < 10:
            return None
        return str(targetSlotX) + "A" + str(targetSlotY)

