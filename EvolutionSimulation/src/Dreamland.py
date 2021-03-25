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
    """

    def __init__(self, size_x=1000, size_y=1000):
        self.sizeX = size_x
        self.sizeY = size_y
        self.populationPlayers = []

    # add population player into this dreamland
    def addPopulationPlayer(self, pt: PopulationThread):
        self.populationPlayers.append(pt)
        pt.run(self)

    # remove population player from this dreamland
    def removePopulationPlayer(self, pt: PopulationThread):
        self.populationPlayers.remove(pt)

    # return slot no. with input x and y coordinates
    @staticmethod
    def returnSlotNo(x, y):
        codeX = (x//10 + 1) * 10
        codeY = (y//10 + 1) * 10
        return str(codeX) + "A" + str(codeY)
