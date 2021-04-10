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
            headerText = ["cycleNumber", "liveIndividuals", "deadIndividuals", "newBorn", "newDeath", "newDeathFromFight", "newDeathFromNatural", "newDeathFromStarve", "breedTimes", "fightTimes", "fightSuccessTimes", "fightPeaceTimes", "fightFailureTimes", "defendTimes", "defendSuccessTimes", "defendPeaceTimes", "defendFailureTimes", "popAvgHungryLevel", "popAvgAge", "popAvgLifespan", "popAvgFightCapability", "popAvgAttackPossibility", "popAvgDefendPossibility", "popAvgTotalBreedingTimes"]
            for i in range(0, len(headerText)):
                sheet.write(0, i, headerText[i], headerStyle)
            rowNum = 1
            threadValue = self.cycleInfo[threadKey]
            for cycleNumber in threadValue.keys():
                cycleInfo = threadValue[cycleNumber]
                sheet.write(rowNum, 0, cycleNumber)
                sheet.write(rowNum, 1, cycleInfo.liveIndividuals)
                sheet.write(rowNum, 2, cycleInfo.deadIndividuals)
                sheet.write(rowNum, 3, cycleInfo.newBorn)
                sheet.write(rowNum, 4, cycleInfo.newDeath)
                sheet.write(rowNum, 5, cycleInfo.newDeathFromFight)
                sheet.write(rowNum, 6, cycleInfo.newDeathFromNatural)
                sheet.write(rowNum, 7, cycleInfo.newDeathFromStarve)
                sheet.write(rowNum, 8, cycleInfo.breedTimes)
                sheet.write(rowNum, 9, cycleInfo.fightTimes)
                sheet.write(rowNum, 10, cycleInfo.fightSuccessTimes)
                sheet.write(rowNum, 11, cycleInfo.fightPeaceTimes)
                sheet.write(rowNum, 12, cycleInfo.fightFailureTimes)
                sheet.write(rowNum, 13, cycleInfo.defendTimes)
                sheet.write(rowNum, 14, cycleInfo.defendSuccessTimes)
                sheet.write(rowNum, 15, cycleInfo.defendPeaceTimes)
                sheet.write(rowNum, 16, cycleInfo.defendFailureTimes)
                sheet.write(rowNum, 17, cycleInfo.popAvgHungryLevel)
                sheet.write(rowNum, 18, cycleInfo.popAvgAge)
                sheet.write(rowNum, 19, cycleInfo.popAvgLifespan)
                sheet.write(rowNum, 20, cycleInfo.popAvgFightCapability)
                sheet.write(rowNum, 21, cycleInfo.popAvgAttackPossibility)
                sheet.write(rowNum, 22, cycleInfo.popAvgDefendPossibility)
                sheet.write(rowNum, 23, cycleInfo.popAvgTotalBreedingTimes)
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
            headerText = ["name", "gender", "generation", "gene", "parents", "age", "birthTime", "deathTime", "deathCause", "populationThreat", "hungryLevel", "lifeStatus", "coordinateX", "coordinateY", "slotCode", "isBusy", "fightTimes", "breedTimes", "moveHistory", "lifespan", "fightCapability", "attackPossibility", "defendPossibility", "totalBreedingTimes"]
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
                    sheet.write(rowNum, 17, ind.breedTimes)
                    sheet.write(rowNum, 18, Recorder.dict2String(ind.moveHistory))
                    sheet.write(rowNum, 19, ind.lifespan)
                    sheet.write(rowNum, 20, ind.fightCapability)
                    sheet.write(rowNum, 21, ind.attackPossibility)
                    sheet.write(rowNum, 22, ind.defendPossibility)
                    sheet.write(rowNum, 23, ind.totalBreedingTimes)
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
                    sheet.write(rowNum, 19, ind.lifespan)
                    sheet.write(rowNum, 20, ind.fightCapability)
                    sheet.write(rowNum, 21, ind.attackPossibility)
                    sheet.write(rowNum, 22, ind.defendPossibility)
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