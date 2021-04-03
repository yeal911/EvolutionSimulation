from EvolutionSimulation.src.population.Population import Population


class Plant:

    # initialize plant thread
    def __init__(self):
        self.coordinateX = 0
        self.coordinateY = 0
        self.slotCode = ""
        self.populationType = Population.PLANT
        self.name = "plant-" + str(id(self))
