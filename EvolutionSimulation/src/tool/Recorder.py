import time

from xlwt import Pattern
import xlwt

from EvolutionSimulation.src.dreamland.Dreamland import Dreamland
from EvolutionSimulation.src.thread.PopulationThread import PopulationThread
from EvolutionSimulation.src.tool.CycleInfo import CycleInfo


class Recorder:
    """this class is used to record all the necessary information during the evolution"""

    def __init__(self, dreamland: Dreamland):
        # cycle info, key is population Thread Name, value is another map (key is cycle number, and value is CycleInfo)
        self.cycleInfo = {}
        self.dreamland = dreamland

    # save cycle information
    def saveCycleInfo(self, cycle_number, pt: PopulationThread, cycle_info: CycleInfo):
        threadRecorder = self.cycleInfo[pt.THREAD_NAME]
        threadRecorder[cycle_number] = cycle_info

    # write all cycle info to excel file
    def writeCycleInfo2File(self):
        workbook = xlwt.Workbook()
        # set header style
        headerStyle = xlwt.XFStyle()
        headerFont = xlwt.Font()
        headerFont.bold = True
        headerStyle.font = headerFont
        headerPattern = Pattern()
        headerPattern.pattern = Pattern.SOLID_PATTERN
        headerPattern.pattern_fore_colour = 50  # green
        headerStyle.pattern = headerPattern
        # write run result to excel file
        for threadKey in self.cycleInfo.keys():
            sheet = workbook.add_sheet(threadKey, True)
            headerText = ["cycleNumber", "liveIndividuals", "deadIndividuals", "newBorn", "newDeath",
                          "newDeathFromFight", "newDeathFromNatural", "newDeathFromStarve", "breedTimes",
                          "fightTimes", "fightSuccessTimes", "fightPeaceTimes", "fightFailureTimes",
                          "FleeSuccessTimes", "defendTimes", "defendSuccessTimes", "defendPeaceTimes",
                          "defendFailureTimes", "popAvgHungryLevel", "popAvgAge", "popAvgLifespan",
                          "popAvgFightCapability", "popAvgAttackPossibility", "popAvgDefendPossibility",
                          "popAvgTotalBreedingTimes", "popAvgCamouflage", "popAvgAttractiveness",
                          "popAvgTerritoryTendency", "kinAltruismTimes", "greenbeardTimes",
                          "pdCooperateTimes", "pdDefectTimes", "sexualRejections", "nestBuilt",
                          "nestUsed", "territoryDefenses", "parasiteAttachments", "parasiteCleared"]
            for i in range(0, len(headerText)):
                sheet.write(0, i, headerText[i], headerStyle)
            rowNum = 1
            threadValue = self.cycleInfo[threadKey]
            for cycleNumber in threadValue.keys():
                cycleInfo = threadValue[cycleNumber]
                col = 0
                sheet.write(rowNum, col, cycleNumber); col += 1
                sheet.write(rowNum, col, cycleInfo.liveIndividuals); col += 1
                sheet.write(rowNum, col, cycleInfo.deadIndividuals); col += 1
                sheet.write(rowNum, col, cycleInfo.newBorn); col += 1
                sheet.write(rowNum, col, cycleInfo.newDeath); col += 1
                sheet.write(rowNum, col, cycleInfo.newDeathFromFight); col += 1
                sheet.write(rowNum, col, cycleInfo.newDeathFromNatural); col += 1
                sheet.write(rowNum, col, cycleInfo.newDeathFromStarve); col += 1
                sheet.write(rowNum, col, cycleInfo.breedTimes); col += 1
                sheet.write(rowNum, col, cycleInfo.fightTimes); col += 1
                sheet.write(rowNum, col, cycleInfo.fightSuccessTimes); col += 1
                sheet.write(rowNum, col, cycleInfo.fightPeaceTimes); col += 1
                sheet.write(rowNum, col, cycleInfo.fightFailureTimes); col += 1
                sheet.write(rowNum, col, cycleInfo.FleeSuccessTimes); col += 1
                sheet.write(rowNum, col, cycleInfo.defendTimes); col += 1
                sheet.write(rowNum, col, cycleInfo.defendSuccessTimes); col += 1
                sheet.write(rowNum, col, cycleInfo.defendPeaceTimes); col += 1
                sheet.write(rowNum, col, cycleInfo.defendFailureTimes); col += 1
                sheet.write(rowNum, col, cycleInfo.popAvgHungryLevel); col += 1
                sheet.write(rowNum, col, cycleInfo.popAvgAge); col += 1
                sheet.write(rowNum, col, cycleInfo.popAvgLifespan); col += 1
                sheet.write(rowNum, col, cycleInfo.popAvgFightCapability); col += 1
                sheet.write(rowNum, col, cycleInfo.popAvgAttackPossibility); col += 1
                sheet.write(rowNum, col, cycleInfo.popAvgDefendPossibility); col += 1
                sheet.write(rowNum, col, cycleInfo.popAvgTotalBreedingTimes); col += 1
                sheet.write(rowNum, col, cycleInfo.popAvgCamouflage); col += 1
                sheet.write(rowNum, col, cycleInfo.popAvgAttractiveness); col += 1
                sheet.write(rowNum, col, cycleInfo.popAvgTerritoryTendency); col += 1
                sheet.write(rowNum, col, cycleInfo.kinAltruismTimes); col += 1
                sheet.write(rowNum, col, cycleInfo.greenbeardTimes); col += 1
                sheet.write(rowNum, col, cycleInfo.pdCooperateTimes); col += 1
                sheet.write(rowNum, col, cycleInfo.pdDefectTimes); col += 1
                sheet.write(rowNum, col, cycleInfo.sexualRejections); col += 1
                sheet.write(rowNum, col, cycleInfo.nestBuilt); col += 1
                sheet.write(rowNum, col, cycleInfo.nestUsed); col += 1
                sheet.write(rowNum, col, cycleInfo.territoryDefenses); col += 1
                sheet.write(rowNum, col, cycleInfo.parasiteAttachments); col += 1
                sheet.write(rowNum, col, cycleInfo.parasiteCleared); col += 1
                rowNum += 1
        workbook.save("EvolutionSimulationResult_" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".xls")

    # write all population info to excel file
    def writePopulationInfo2File(self):
        workbook = xlwt.Workbook()
        # set header style
        headerStyle = xlwt.XFStyle()
        headerFont = xlwt.Font()
        headerFont.bold = True
        headerStyle.font = headerFont
        headerPattern = Pattern()
        headerPattern.pattern = Pattern.SOLID_PATTERN
        headerPattern.pattern_fore_colour = 50  # green
        headerStyle.pattern = headerPattern
        # write run result to excel file

        for thread in self.dreamland.populationThreadPlayers:
            sheet = workbook.add_sheet(thread.THREAD_NAME, True)
            headerText = ["name", "gender", "generation", "gene", "parents", "age", "birthTime", "deathTime",
                          "deathCause", "populationThreat", "hungryLevel", "lifeStatus", "coordinateX",
                          "coordinateY", "slotCode", "isBusy", "fightTimes", "fleeSuccessTimes",
                          "fleeFailureTimes", "breedTimes", "moveHistory", "lifespan", "fightCapability",
                          "attackPossibility", "defendPossibility", "totalBreedingTimes", "camouflage",
                          "greenbeardBadge", "attractiveness", "territoryTendency", "pdStrategy", "reputation"]
            for i in range(0, len(headerText)):
                sheet.write(0, i, headerText[i], headerStyle)
            rowNum = 1
            if thread.THREAD_TYPE == "Animal":
                for ind in (thread.group + thread.dead):
                    sheet.write(rowNum, 0, ind.name)
                    sheet.write(rowNum, 1, ind.gender)
                    sheet.write(rowNum, 2, ind.generation)
                    sheet.write(rowNum, 3, Recorder.list2String(ind.gene.geneDigits))
                    sheet.write(rowNum, 4, ind.parents)
                    sheet.write(rowNum, 5, ind.age)
                    sheet.write(rowNum, 6, ind.birthTime)
                    sheet.write(rowNum, 7, ind.deathTime)
                    sheet.write(rowNum, 8, ind.deathCause)
                    sheet.write(rowNum, 9, ind.populationThreat)
                    sheet.write(rowNum, 10, ind.hungryLevel)
                    sheet.write(rowNum, 11, ind.lifeStatus)
                    sheet.write(rowNum, 12, ind.coordinateX)
                    sheet.write(rowNum, 13, ind.coordinateY)
                    sheet.write(rowNum, 14, ind.slotCode)
                    sheet.write(rowNum, 15, ind.isBusy)
                    sheet.write(rowNum, 16, ind.fightTimes)
                    sheet.write(rowNum, 17, ind.fleeSuccessTimes)
                    sheet.write(rowNum, 18, ind.fleeFailureTimes)
                    sheet.write(rowNum, 19, ind.breedTimes)
                    sheet.write(rowNum, 20, Recorder.dict2String(ind.moveHistory))
                    sheet.write(rowNum, 21, ind.lifespan)
                    sheet.write(rowNum, 22, ind.fightCapability)
                    sheet.write(rowNum, 23, ind.attackPossibility)
                    sheet.write(rowNum, 24, ind.defendPossibility)
                    sheet.write(rowNum, 25, ind.totalBreedingTimes)
                    sheet.write(rowNum, 26, getattr(ind, 'camouflage', 0))
                    sheet.write(rowNum, 27, getattr(ind, 'greenbeardBadge', 0))
                    sheet.write(rowNum, 28, getattr(ind, 'attractiveness', 0))
                    sheet.write(rowNum, 29, getattr(ind, 'territoryTendency', 0))
                    sheet.write(rowNum, 30, getattr(ind, 'pdStrategy', 0))
                    sheet.write(rowNum, 31, getattr(ind, 'reputation', 0))
                    rowNum += 1
            elif thread.THREAD_TYPE == "Plant":
                for ind in (thread.group + thread.dead):
                    sheet.write(rowNum, 0, ind.name)
                    sheet.write(rowNum, 5, ind.age)
                    sheet.write(rowNum, 6, ind.birthTime)
                    sheet.write(rowNum, 7, ind.deathTime)
                    sheet.write(rowNum, 8, ind.deathCause)
                    sheet.write(rowNum, 9, ind.populationThreat)
                    sheet.write(rowNum, 11, ind.lifeStatus)
                    sheet.write(rowNum, 12, ind.coordinateX)
                    sheet.write(rowNum, 13, ind.coordinateY)
                    sheet.write(rowNum, 14, ind.slotCode)
                    sheet.write(rowNum, 15, ind.isBusy)
                    sheet.write(rowNum, 16, ind.fightTimes)
                    sheet.write(rowNum, 21, ind.lifespan)
                    sheet.write(rowNum, 22, ind.fightCapability)
                    sheet.write(rowNum, 23, ind.attackPossibility)
                    sheet.write(rowNum, 24, ind.defendPossibility)
                    rowNum += 1
        workbook.save("EvolutionSimulationIndividuals_" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".xls")

    @staticmethod
    def dict2String(dict_map: {}):
        returnValue = ""
        for key in dict_map:
            returnValue += str(key) + "," + dict_map[key] + ";"
        return returnValue

    @staticmethod
    def list2String(listArray: []):
        returnValue = ""
        for tmp in listArray:
            returnValue += str(tmp) + ","
        return returnValue
