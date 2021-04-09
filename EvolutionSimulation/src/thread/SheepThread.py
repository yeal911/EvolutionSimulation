import threading

from EvolutionSimulation.src.thread.PopulationThread import PopulationThread
from EvolutionSimulation.src.tool.Recorder import Recorder
from EvolutionSimulation.src.dreamland.Dreamland import Dreamland
from EvolutionSimulation.src.population.Sheep import Sheep


class SheepThread(threading.Thread, PopulationThread):
    """
    Thread for sheep population, to evolute all the individuals of sheep population

    ***parameter explanation***
    dreamland: where this thread runs
    initCount: initiate the sheep count to be loaded to dream land
    coordinateX: x coordinate in dream land
    coordinateY: y coordinate in dream land
    slotCode: slot code computed
    group: all the individuals
    dead: all dead individuals
    """
    THREAD_NAME = "SheepThread"
    THREAD_TYPE = "Animal"

    # initialize sheep thread
    def __init__(self, sheep_count, dreamland: Dreamland, recorder: Recorder):
        threading.Thread.__init__(self)
        self.dreamland = dreamland
        self.recorder = recorder
        self.continueRunning = True
        self.initCount = sheep_count
        self.group = []
        self.dead = []
        self.num = []
        self.newBronNum = []
        self.newDeathNum = []
        self.avgHungryLevel = []
        self.avgLifespan = []
        self.avgFightCapability = []
        self.avgAge = []
        self.avgAttackPossibility = []
        self.avgDefendPossibility = []
        self.avgTotalBreedingTimes =[]
        self.cycleNumber = 0
        for i in range(0, sheep_count):
            # need to randomly initialize the coordinates of the sheep
            sheep = Sheep()
            self.addIndividual2Thread(sheep)
        # add sheep thread to dreamland
        self.dreamland.populationThreadPlayers.append(self)
        # initialize recorder to record every cycle info
        self.recorder.cycleInfo[SheepThread.THREAD_NAME] = {}

    # monitor all individuals, and execute for all their actions
    def run(self):
        self.animalThreadRun()