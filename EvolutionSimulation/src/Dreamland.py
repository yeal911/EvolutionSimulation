#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt

from EvolutionSimulation.src.Population import PopulationThread


class Dreamland:
    """the playground of all populations, with X & Y coordinates"""
    # # dreamland size X
    # __sizeX__ = 1000
    # # dreamland size Y
    # __sizeY__ = 1000

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