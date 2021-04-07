from EvolutionSimulation.src.dreamland.Dreamland import Dreamland
from EvolutionSimulation.src.thread.PlantThread import PlantSet
from EvolutionSimulation.src.thread.SheepThread import SheepThread

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



