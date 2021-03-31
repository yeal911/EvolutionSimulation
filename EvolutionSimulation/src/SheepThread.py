import threading
import time
import random

from EvolutionSimulation.src.Dreamland import Dreamland
from EvolutionSimulation.src.PopulationThread import PopulationThread
from EvolutionSimulation.src.Sheep import Sheep


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

       """

    # initialize sheep thread
    def __init__(self, sheep_count, dreamland: Dreamland):
        threading.Thread.__init__(self)
        self.dreamland = dreamland
        self.initCount = sheep_count
        self.group = []
        self.dead = []
        for i in range(0, sheep_count):
            # need to randomly initialize the coordinates of the sheep
            sheep = Sheep()
            sheep.coordinateX = random.randint(0, Dreamland.SIZE_X)
            sheep.coordinateY = random.randint(0, Dreamland.SIZE_Y)
            # set the slot code in the dreamland
            sheep.slotCode = Dreamland.returnSlotNo(sheep.coordinateX, sheep.coordinateY)
            print("sheep.SlotCode is " + str(sheep.slotCode))
            self.group.append(sheep)
            # update coordinate map
            self.updateDreamLandMap(sheep, None, sheep.slotCode)
        # add sheep thread to dreamland
        # self.dreamland.populationPlayers.append()

    def run(self):
        time.sleep(1)
        for sheep in self.group:
            # add logic for forage, find for food if it is hungry
            if sheep.hungryLevel > 5:
                # find food in its own slot, if there is, then flight, if none, change position
                print(sheep.name + " hungryLevel: " + str(sheep.hungryLevel))
            else:
                print(sheep.name + " hungryLevel: " + str(sheep.hungryLevel))
