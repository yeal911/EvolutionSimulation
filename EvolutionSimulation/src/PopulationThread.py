#!/usr/bin/python3
from abc import ABCMeta, abstractmethod


class PopulationThread(metaclass=ABCMeta):
    """this abstract class defines the common actions of population thread"""

    # # return individual count of a population in the Thread
    # @abstractmethod
    # def getIndividualCount(self): pass

    # run for population thread
    @abstractmethod
    def run(self): pass