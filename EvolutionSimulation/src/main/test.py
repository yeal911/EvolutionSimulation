import time

from EvolutionSimulation.src.dreamland.Dreamland import Dreamland
from EvolutionSimulation.src.thread.TigerThread import TigerThread
from EvolutionSimulation.src.thread.WolfThread import WolfThread
from EvolutionSimulation.src.tool.Recorder import Recorder

dreamland = Dreamland()
recorder = Recorder()
wolfThread = WolfThread(50, dreamland, recorder)
tigerThread = TigerThread(10, dreamland, recorder)

Dreamland.startPopulationThread(wolfThread)
Dreamland.startPopulationThread(tigerThread)
start = time.time()
while True:
    time.sleep(1)
    end = time.time()
    print("---Time elapses: " + str(int(end - start)))
    if end - start > 500:
        recorder.writeInfo2File()
        Dreamland.stopPopulationThread(tigerThread)
        Dreamland.stopPopulationThread(wolfThread)
        break