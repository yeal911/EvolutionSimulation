import time

from EvolutionSimulation.src.dreamland.Dreamland import Dreamland
from EvolutionSimulation.src.thread.TigerThread import TigerThread
from EvolutionSimulation.src.thread.WolfThread import WolfThread
from EvolutionSimulation.src.tool.Recorder import Recorder

dreamland = Dreamland()
recorder = Recorder()
wolfThread = WolfThread(20, dreamland, recorder)
tigerThread = TigerThread(10, dreamland, recorder)

Dreamland.startPopulationThread(wolfThread)
Dreamland.startPopulationThread(tigerThread)
start = time.time()
while True:
    end = time.time()
    if end - start > 200:
        dreamland.stopPopulationThread(wolfThread)
        dreamland.stopPopulationThread(tigerThread)
        recorder.writeInfo2File()
        break