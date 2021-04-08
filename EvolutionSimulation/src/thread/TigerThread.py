import threading

from EvolutionSimulation.src.thread.PopulationThread import PopulationThread
from EvolutionSimulation.src.tool.Recorder import Recorder
from EvolutionSimulation.src.dreamland.Dreamland import Dreamland
from EvolutionSimulation.src.population.Tiger import Tiger


class TigerThread(threading.Thread, PopulationThread):
    """
    Thread for tiger population, to evolute all the individuals of tiger population

    ***parameter explanation***
    dreamland: where this thread runs
    initCount: initiate the tiger count to be loaded to dream land
    coordinateX: x coordinate in dream land
    coordinateY: y coordinate in dream land
    slotCode: slot code computed
    group: all the individuals
    dead: all dead individuals
    """
    THREAD_NAME = "TigerThread"
    THREAD_TYPE = "Animal"

    # initialize tiger thread
    def __init__(self, tiger_count, dreamland: Dreamland, recorder: Recorder):
        threading.Thread.__init__(self)
        self.dreamland = dreamland
        self.recorder = recorder
        self.continueRunning = True
        self.initCount = tiger_count
        self.group = []
        self.dead = []
        self.num = []
        self.cycleNumber = 0
        for i in range(0, tiger_count):
            # need to randomly initialize the coordinates of the tiger
            tiger = Tiger()
            self.addIndividual2Thread(tiger)
        # add tiger thread to dreamland
        self.dreamland.populationThreadPlayers.append(self)
        # initialize recorder to record every cycle info
        self.recorder.cycleInfo[TigerThread.THREAD_NAME] = {}

    # monitor all individuals, and execute for all their actions
    def run(self):
        self.animalThreadRun()