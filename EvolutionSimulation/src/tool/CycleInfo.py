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
        self.newDeathFromFight = 0
        self.newDeathFromNatural = 0
        self.newDeathFromStarve = 0
        self.breedTimes = 0
        self.fightTimes = 0
        self.defendTimes = 0
        self.fightSuccessTimes = 0
        self.fightPeaceTimes = 0
        self.fightFailureTimes = 0
        self.FleeSuccessTimes = 0
        self.defendSuccessTimes = 0
        self.defendPeaceTimes = 0
        self.defendFailureTimes = 0

        # New stats for enhanced features
        self.kinAltruismTimes = 0
        self.greenbeardTimes = 0
        self.pdCooperateTimes = 0
        self.pdDefectTimes = 0
        self.sexualRejections = 0
        self.nestBuilt = 0
        self.nestUsed = 0
        self.territoryDefenses = 0
        self.parasiteAttachments = 0
        self.parasiteCleared = 0
        self.camouflageSuccess = 0

        # average info of a population in one cycle
        self.popAvgHungryLevel = 0
        self.popAvgAge = 0
        self.popAvgLifespan = 0
        self.popAvgFightCapability = 0
        self.popAvgAttackPossibility = 0
        self.popAvgDefendPossibility = 0
        self.popAvgTotalBreedingTimes = 0
        self.popAvgCamouflage = 0
        self.popAvgAttractiveness = 0
        self.popAvgTerritoryTendency = 0
