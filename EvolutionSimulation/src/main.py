from EvolutionSimulation.src.Dreamland import Dreamland
from EvolutionSimulation.src.PlantSet import PlantSet
from EvolutionSimulation.src.SheepThread import SheepThread
from WolfThread import WolfThread

dreamLand = Dreamland()
# dreamLand1 = Dreamland()
plantSet = PlantSet(50, dreamLand)

print("plant1 length is " + str(len(plantSet.group)))
sheepThread = SheepThread(5, dreamLand, plantSet)

# wolfThread = WolfThread(2, dreamLand)

dreamLand.startPopulationThread(sheepThread)

# dreamLand.addPopulationPlayer(wolfThread)

# print("sheepThread.group[0]" + sheepThread.group[0].gender)
# print("sheepThread.group[1]" + sheepThread.group[1].gender)
#
# spouse = sheepThread.searchSpouse(sheepThread.group[0])
# print("spouse " + str(spouse))



