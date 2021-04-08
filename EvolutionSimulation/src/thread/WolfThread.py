import threading

from EvolutionSimulation.src.thread.PopulationThread import PopulationThread
from EvolutionSimulation.src.tool.Recorder import Recorder
from EvolutionSimulation.src.dreamland.Dreamland import Dreamland
from EvolutionSimulation.src.population.Wolf import Wolf


class WolfThread(threading.Thread, PopulationThread):
    """
    Thread for wolf population, to evolute all the individuals of wolf population

    ***parameter explanation***
    dreamland: where this thread runs
    initCount: initiate the wolf count to be loaded to dream land
    coordinateX: x coordinate in dream land
    coordinateY: y coordinate in dream land
    slotCode: slot code computed
    group: all the individuals
    dead: all dead individuals
    """
    THREAD_NAME = "WolfThread"
    THREAD_TYPE = "Animal"

    # initialize wolf thread
    def __init__(self, wolf_count, dreamland: Dreamland, recorder: Recorder):
        threading.Thread.__init__(self)
        self.dreamland = dreamland
        self.recorder = recorder
        self.continueRunning = True
        self.initCount = wolf_count
        self.group = []
        self.dead = []
        self.num = []
        self.cycleNumber = 0
        for i in range(0, wolf_count):
            # need to randomly initialize the coordinates of the wolf
            wolf = Wolf()
            self.addIndividual2Thread(wolf)
        # add wolf thread to dreamland
        self.dreamland.populationThreadPlayers.append(self)
        # initialize recorder to record every cycle info
        self.recorder.cycleInfo[WolfThread.THREAD_NAME] = {}

    # monitor all individuals, and execute for all their actions
    def run(self):
        self.animalThreadRun()