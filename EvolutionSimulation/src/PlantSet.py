import random

import Dreamland
from EvolutionSimulation.src.Plant import Plant
from EvolutionSimulation.src.PopulationThread import PopulationThread


class PlantSet(PopulationThread):

    # initialize plant thread
    def __init__(self, plant_count, dreamland: Dreamland):
        self.dreamland = dreamland
        self.initCount = plant_count
        self.group = []
        self.dead = []

        # need to randomly initialize the coordinates of the plant
        for i in range(0, plant_count):
            plant = Plant()
            plant.coordinateX = random.randint(0, Dreamland.Dreamland.SIZE_X - 1)
            plant.coordinateY = random.randint(0, Dreamland.Dreamland.SIZE_Y - 1)
            # set the slot code in the dreamland
            plant.slotCode = Dreamland.Dreamland.returnSlotNo(plant.coordinateX, plant.coordinateY)
            print("plant.SlotCode is " + str(plant.slotCode))
            self.group.append(plant)
            # update coordinate map
            self.updateDreamLandMap(plant, None, plant.slotCode)
        # add plant thread to dreamland
        self.dreamland.populationThreadPlayers.append(self)
