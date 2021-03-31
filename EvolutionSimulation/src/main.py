from EvolutionSimulation.src.Dreamland import Dreamland
from EvolutionSimulation.src.SheepThread import SheepThread
from EvolutionSimulation.src.Wolf import WolfThread

dreamLand = Dreamland()
# dreamLand1 = Dreamland()
# for i in len(dreamLand.coordinateMap):
print(dreamLand.coordinateMap)
print(len(dreamLand.coordinateMap))
sheepThread = SheepThread(2, dreamLand)
# wolfThread = WolfThread(2, dreamLand)


dreamLand.addPopulationPlayer(sheepThread)

# dreamLand.addPopulationPlayer(wolfThread)

print("sheepThread.group[0]" + sheepThread.group[0].gender)
print("sheepThread.group[1]" + sheepThread.group[1].gender)

spouse = sheepThread.searchSpouse(sheepThread.group[0])
print("spouse " + str(spouse))



