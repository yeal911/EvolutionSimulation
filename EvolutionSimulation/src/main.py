from EvolutionSimulation.src.Dreamland import Dreamland
from EvolutionSimulation.src.SheepThread import SheepThread
from EvolutionSimulation.src.Wolf import WolfThread

dreamLand = Dreamland()
dreamLand1 = Dreamland()

sheepThread = SheepThread(2, dreamLand)
wolfThread = WolfThread(2, dreamLand1)
#
#
# dreamLand.addPopulationPlayer(sheepThread)
# print("dreamland " + str(dreamLand))
#
# dreamLand.addPopulationPlayer(wolfThread)
# print("dreamland " + str(dreamLand1))




