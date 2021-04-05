#!/usr/bin/python3
# from abc import ABCMeta, abstractmethod
import time


class Population:
    """this abstract class defines the common actions of population"""

    # defines the population feeding types
    CARNIVORE = 1
    HERBIVORE = 2

    # defines the population types
    ANIMAL = 1
    PLANT = 2

    # # forage behaviour of a population
    # @abstractmethod
    # def forage(self): pass
    #
    # # grow behaviour of a population
    # @abstractmethod
    # def grow(self): pass

    # attack behaviour of a population
    # fight behaviour of a wolf
    def fight(self, competitor):
        if self.fightCapability > competitor.fightCapability:
            # win fight, reset properties
            self.hungryLevel = 0
            self.fightTimes += 1
            competitor.ownThread.receiveDefendInfo("Failure", competitor)
            return "Success"
        elif self.fightCapability == competitor.fightCapability:
            self.hungryLevel += 1
            competitor.ownThread.receiveDefendInfo("Peace", competitor)
            return "Peace"
        else:
            competitor.ownThread.receiveDefendInfo("Success", competitor)
            self.fightTimes += 1
            self.lifeStatus = "Dead"
            self.deathCause = "Fight to death"
            self.deathTime = time.time()
            return "Failure"

    # # defend behaviour of a population
    # @abstractmethod
    # def defend(self): pass

    # # breed behaviour of a population
    # @abstractmethod
    # def breed(self, spouse): pass