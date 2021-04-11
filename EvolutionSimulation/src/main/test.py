import time

from EvolutionSimulation.src.dreamland.Dreamland import Dreamland
from EvolutionSimulation.src.thread.PlantThread import PlantThread
from EvolutionSimulation.src.thread.SheepThread import SheepThread
from EvolutionSimulation.src.thread.TigerThread import TigerThread
from EvolutionSimulation.src.thread.WolfThread import WolfThread
from EvolutionSimulation.src.tool.Recorder import Recorder

dreamland = Dreamland()
recorder = Recorder(dreamland)
plantThread = PlantThread(100, dreamland, recorder)
sheepThread = SheepThread(500, dreamland, recorder)
wolfThread = WolfThread(500, dreamland, recorder)
tigerThread = TigerThread(50, dreamland, recorder)

Dreamland.startPopulationThread(plantThread)
Dreamland.startPopulationThread(sheepThread)
Dreamland.startPopulationThread(wolfThread)
Dreamland.startPopulationThread(tigerThread)
start = time.time()
while True:
    time.sleep(1)
    end = time.time()
    print("---Time elapses: " + str(int(end - start)))
    if end - start > 60:
        Dreamland.stopPopulationThread(plantThread)
        Dreamland.stopPopulationThread(sheepThread)
        Dreamland.stopPopulationThread(tigerThread)
        Dreamland.stopPopulationThread(wolfThread)
        recorder.writeCycleInfo2File()
        recorder.writePopulationInfo2File()
        break
    elif len(wolfThread.group) == 0 and len(tigerThread.group) == 0 and len(sheepThread.group) == 0:
        Dreamland.stopPopulationThread(plantThread)
        Dreamland.stopPopulationThread(sheepThread)
        Dreamland.stopPopulationThread(tigerThread)
        Dreamland.stopPopulationThread(wolfThread)
        recorder.writeCycleInfo2File()
        recorder.writePopulationInfo2File()
        break

print("sheep group " + str(len(sheepThread.group)))
print("wolf group " + str(len(wolfThread.group)))
print("tiger group " + str(len(tigerThread.group)))