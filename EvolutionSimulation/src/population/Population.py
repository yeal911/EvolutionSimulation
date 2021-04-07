#!/usr/bin/python3
# from abc import ABCMeta, abstractmethod
import time

from EvolutionSimulation.src.gene.Gene import Gene


class Population:
    """this abstract class defines the common actions of population"""

    # defines the population feeding types
    CARNIVORE = 1
    HERBIVORE = 2

    # defines the population types
    ANIMAL = 1
    PLANT = 2

    # fight behaviour of a population individual
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
            self.deathTime = time.strftime("%Y%m%d%H%M%S%f", time.localtime())
            return "Failure"

    # breed behaviour of a tiger
    def breed(self, spouse):
        if spouse.__class__.__name__ != self.__class__.__name__ or self.gender == spouse.gender:
            print("Different population or same gender, no breed")
            return None
        if (self.breedTimes <= self.TotalBreedingTimes and self.lowerGrowthPeriod < self.age < self.upperGrowthPeriod) and (spouse.breedTimes <= spouse.TotalBreedingTimes and spouse.lowerGrowthPeriod < spouse.age < spouse.upperGrowthPeriod):
            self.breedTimes += 1
            spouse.breedTimes += 1
            self.hungryLevel += 1
            spouse.hungryLevel += 1
            # rebuild gene_set for new baby tiger, get first half gene set from self, another half from spouse
            childGeneDigits = []
            # get first half gene set from self after variation
            parentX = self.gene.variate()
            parentY = spouse.gene.variate()
            for i in range(0, Gene.GENE_LENGTH, 2):
                childGeneDigits.append(parentX.geneDigits[i])
                childGeneDigits.append(parentY.geneDigits[i+1])
            return self.newChild(Gene(childGeneDigits), round((self.generation + spouse.generation) / 2), self.name + "/" + spouse.name)
        return None