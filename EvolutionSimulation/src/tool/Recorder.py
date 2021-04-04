#!/usr/bin/python3
from EvolutionSimulation.src.thread.PopulationThread import PopulationThread
from EvolutionSimulation.src.tool.CycleInfo import CycleInfo


class Recorder:
    """this class is used to record all the necessary information during the evolution"""

    def __init__(self):
        # cycle info, key is population Thread Name, value is another map (key is cycle number, and value is CycleInfo)
        self.cycleInfo = {}

    # save cycle information
    def saveCycleInfo(self, cycle_number, pt: PopulationThread, cycle_info: CycleInfo):
        threadRecorder = self.cycleInfo[pt.THREAD_NAME]
        threadRecorder[cycle_number] = cycle_info

    # write all info to excel file
    def writeInfo2File(self): pass