# from abc import ABCMeta, abstractmethod
import math
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
        # if competitor is animal, check if competitor will try to escape
        if competitor.populationType == Population.ANIMAL:
            # competitor will try to flee
            if self.populationThreat - competitor.populationThreat >= 2:
                distance = math.sqrt(math.pow(self.coordinateX - competitor.coordinateX, 2) + math.pow(self.coordinateY - competitor.coordinateY, 2))
                # competitor escapes successful
                if self.runningSpeed <= competitor.runningSpeed or distance * 10 / (self.runningSpeed - competitor.runningSpeed) > 10:
                    competitor.fleeSuccessTimes += 1
                    # print("Flee")
                    return "Flee"
                else:
                    competitor.fleeFailureTimes += 1
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
            self.deathTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
            return "Failure"

    # breed behaviour of an animal population individual
    def breed(self, spouse):
        if spouse.__class__.__name__ != self.__class__.__name__ or self.gender == spouse.gender:
            print("Different population or same gender, no breed")
            return None
        if (self.breedTimes <= self.totalBreedingTimes and self.lowerGrowthPeriod < self.age < self.upperGrowthPeriod) and (spouse.breedTimes <= spouse.totalBreedingTimes and spouse.lowerGrowthPeriod < spouse.age < spouse.upperGrowthPeriod):
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
            return self.newChild(Gene(childGeneDigits), math.ceil((self.generation + spouse.generation) / 2 + 1), self.name + "/" + spouse.name)
        return None