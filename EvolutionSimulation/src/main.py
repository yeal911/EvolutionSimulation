from EvolutionSimulation.src.Dreamland import Dreamland
from EvolutionSimulation.src.SheepThread import SheepThread

dreamLand = Dreamland()
sheepThread = SheepThread(2, dreamLand)


dreamLand.addPopulationPlayer(sheepThread)
# print("dreamLand.coordinateMap.get()" +  + dreamLand.coordinateMap.get("10A10"))

