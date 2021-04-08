import threading
import time

from EvolutionSimulation.src.thread.PopulationThread import PopulationThread
from EvolutionSimulation.src.tool.CycleInfo import CycleInfo
from EvolutionSimulation.src.tool.Recorder import Recorder
from EvolutionSimulation.src.dreamland.Dreamland import Dreamland
from EvolutionSimulation.src.population.Plant import Plant


class PlantThread(threading.Thread, PopulationThread):
    """
    Thread for plant population, to evolute all the individuals of plant population

    ***parameter explanation***
    dreamland: where this thread runs
    initCount: initiate the plant count to be loaded to dream land
    coordinateX: x coordinate in dream land
    coordinateY: y coordinate in dream land
    slotCode: slot code computed
    group: all the individuals
    dead: all dead individuals
    """
    THREAD_NAME = "PlantThread"
    THREAD_TYPE = "Plant"

    # initialize plant thread
    def __init__(self, cycle_plant_count, dreamland: Dreamland, recorder: Recorder):
        threading.Thread.__init__(self)
        self.dreamland = dreamland
        self.recorder = recorder
        self.continueRunning = True
        self.cyclePlantCount = cycle_plant_count
        self.group = []
        self.dead = []
        self.cycleNumber = 0
        for i in range(0, self.cyclePlantCount):
            # need to randomly initialize the coordinates of the plant
            plant = Plant()
            self.addIndividual2Thread(plant)
        # add plant thread to dreamland
        self.dreamland.populationThreadPlayers.append(self)
        # initialize recorder to record every cycle info
        self.recorder.cycleInfo[PlantThread.THREAD_NAME] = {}

    # monitor all individuals, and execute for all their actions
    def run(self):
        self.plantThreadRun()