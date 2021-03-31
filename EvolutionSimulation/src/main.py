from EvolutionSimulation.src.Dreamland import Dreamland
from EvolutionSimulation.src.SheepThread import SheepThread
from EvolutionSimulation.src.Wolf import WolfThread

dreamLand = Dreamland()
sheepThread = SheepThread(2, dreamLand)
wolfThread = WolfThread(2, dreamLand)


dreamLand.addPopulationPlayer(sheepThread)
dreamLand.addPopulationPlayer(wolfThread)




