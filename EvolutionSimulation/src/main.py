from EvolutionSimulation.src.Dreamland import Dreamland
from EvolutionSimulation.src.SheepThread import SheepThread

dreamLand = Dreamland()
sheepThread = SheepThread(5, dreamLand)

print(dreamLand.coordinateMap.get("10A10"))

dreamLand.addPopulationPlayer(sheepThread)

print("dreamLand.SIZE_X is " + str(dreamLand.SIZE_X))
print("dreamLand.SIZE_Y is " + str(dreamLand.SIZE_Y))
