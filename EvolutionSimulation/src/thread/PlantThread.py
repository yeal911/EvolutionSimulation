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
        while self.continueRunning:
            print(self.THREAD_NAME + " cycle: " + str(self.cycleNumber + 1) + ".  Remaining individual: " + str(len(self.group)))
            self.cycleNumber += 1
            cycleInfo = CycleInfo(self.THREAD_NAME)
            # generate new plants in each round if plants count is less than 10 times of the slots
            if len(self.group) < int(Dreamland.SIZE_X * Dreamland.SIZE_Y) / 100 * 10:
                for i in range(0, self.cyclePlantCount):
                    # need to randomly initialize the coordinates of the plant
                    plant = Plant()
                    self.addIndividual2Thread(plant)
                cycleInfo.newBorn = self.cyclePlantCount
            if len(self.group) != 0:
                for individual in self.group:
                    # check if individual should die naturally
                    if individual.age >= individual.lifespan:
                        individual.lifeStatus = "Dead"
                        individual.deathCause = "Natural death"
                        cycleInfo.newDeathFromNatural += 1
                    elif individual.deathCause == "Fight to death":
                        cycleInfo.newDeathFromFight += 1
                    # check individual life status first, move to different category if dead (starve to death/natural death/fight to death)
                    if individual.lifeStatus == "Dead":
                        individual.deathTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
                        self.group.remove(individual)
                        self.dead.append(individual)
                        cycleInfo.newDeath += 1
                        continue
                    individual.age += 1
                    cycleInfo.popAvgAge += individual.age
                    cycleInfo.popAvgLifespan += individual.lifespan
                    cycleInfo.popAvgFightCapability += individual.fightCapability
                    cycleInfo.popAvgAttackPossibility += individual.attackPossibility
                    cycleInfo.popAvgDefendPossibility += individual.defendPossibility
            # if there is still live population
            cycleInfo.liveIndividuals = len(self.group)
            cycleInfo.deadIndividuals = len(self.dead)
            if len(self.group) != 0:
                cycleInfo.popAvgAge = round(cycleInfo.popAvgAge / len(self.group), 2)
                cycleInfo.popAvgLifespan = round(cycleInfo.popAvgLifespan / len(self.group), 2)
                cycleInfo.popAvgFightCapability = round(cycleInfo.popAvgFightCapability / len(self.group), 2)
                cycleInfo.popAvgAttackPossibility = round(cycleInfo.popAvgAttackPossibility / len(self.group), 2)
                cycleInfo.popAvgDefendPossibility = round(cycleInfo.popAvgDefendPossibility / len(self.group), 2)
            self.recorder.saveCycleInfo(self.cycleNumber, self, cycleInfo)
            # sleep for 1 day (1s)
            time.sleep(1)