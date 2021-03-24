#!/usr/bin/python3

from abc import ABCMeta, abstractmethod

from EvolutionSimulation.src.Dreamland import Dreamland


class Population(metaclass=ABCMeta):
    """this abstract class defines the common actions of population"""

    # forage behaviour of a population
    @abstractmethod
    def forage(self): pass

    # grow behaviour of a population
    @abstractmethod
    def grow(self): pass

    # attack behaviour of a population
    @abstractmethod
    def fight(self, population): pass

    # # defend behaviour of a population
    # @abstractmethod
    # def defend(self): pass

    # breed behaviour of a population
    @abstractmethod
    def breed(self, spouse): pass


class PopulationThread(metaclass=ABCMeta):
    """this abstract class defines the common actions of population thread"""

    # return individual count of a population in the Thread
    @abstractmethod
    def getIndividualCount(self): pass

    # run for population thread
    @abstractmethod
    def run(self, dreamland: Dreamland): pass