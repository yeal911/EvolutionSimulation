import threading
import time
import random

from EvolutionSimulation.src.Dreamland import Dreamland
from EvolutionSimulation.src.PlantSet import PlantSet
from EvolutionSimulation.src.Population import Population
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
    def __init__(self, sheep_count, dreamland: Dreamland, plantSet: PlantSet):
        threading.Thread.__init__(self)
        self.dreamland = dreamland
        self.initCount = sheep_count
        self.group = []
        self.dead = []
        self.plantSet = plantSet
        for i in range(0, sheep_count):
            # need to randomly initialize the coordinates of the sheep
            sheep = Sheep()
            sheep.coordinateX = random.randint(0, Dreamland.SIZE_X - 1)
            sheep.coordinateY = random.randint(0, Dreamland.SIZE_Y - 1)
            # set the slot code in the dreamland
            sheep.slotCode = Dreamland.returnSlotCode(sheep.coordinateX, sheep.coordinateY)
            print("sheep.SlotCode is " + str(sheep.slotCode))
            self.group.append(sheep)
            # update coordinate map
            self.updateDreamLandMap(sheep, None, sheep.slotCode)
        # add sheep thread to dreamland
        self.dreamland.populationThreadPlayers.append(self)

    def run(self):
        time.sleep(1)
        for sheep in self.group:
            # add logic for forage, find for food if it is hungry
            if sheep.hungryLevel > 5:
                # find food in its own slot, if there is, then flight, if none, change position
                food = self.searchFood(sheep)
                if food is not None:
                    print("food is " + str(food))
                    sheep.hungryLevel -= 1
                    if food.populationType == Population.PLANT:
                        self.plantSet.group.remove(food)
                        print(sheep.name + " forage successfully! hungryLevel: " + str(sheep.hungryLevel))
                        print("plant2 length is " + str(len(self.plantSet.group)))
            else:
                sheep.hungryLevel += 1
                print(sheep.name + " hungryLevel: " + str(sheep.hungryLevel))

            # add logic for breed
            spouse = self.searchSpouse(sheep)
            if spouse is not None:
                newSheep = sheep.breed(spouse)
                if newSheep is not None:
                    # self.group.append(newSheep)
                    newSheep.coordinateX = random.randint(0, Dreamland.SIZE_X - 1)
                    newSheep.coordinateY = random.randint(0, Dreamland.SIZE_Y - 1)
                    # set the slot code in the dreamland
                    newSheep.slotCode = Dreamland.returnSlotCode(newSheep.coordinateX, newSheep.coordinateY)
                    print("newSheep.SlotCode is " + str(sheep.slotCode))
                    self.group.append(newSheep)
                    # update coordinate map
                    self.updateDreamLandMap(newSheep, None, newSheep.slotCode)


