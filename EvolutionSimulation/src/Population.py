#!/usr/bin/python3
from abc import ABCMeta, abstractmethod


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