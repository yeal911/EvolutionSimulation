#!/usr/bin/python3

class CycleInfo:
    """defines all the cycle info"""

    def __init__(self, population_type):
        # indicate what population it is
        self.populationType = population_type

        # statistics info of a population in one cycle
        self.liveIndividuals = 0
        self.deadIndividuals = 0
        self.newBorn = 0
        self.newDeath = 0
        self.breedTimes = 0
        self.fightTimes = 0
        self.defendTimes = 0
        self.fightSuccessTimes = 0
        self.fightPeaceTimes = 0
        self.fightFailureTimes = 0
        self.defendSuccessTimes = 0
        self.defendPeaceTimes = 0
        self.defendFailureTimes = 0

        # average info of a population in one cycle
        self.popAvgHungryLevel = 0
        self.popAvgAge = 0
        self.popAvgLifespan = 0
        self.popAvgFightCapability = 0
        self.popAvgAttackPossibility = 0
        self.popAvgDefendPossibility = 0
        self.popAvgTotalBreedingTimes = 0