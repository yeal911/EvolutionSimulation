import time

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Signal, QObject, QTimer
import pyqtgraph as pg
from threading import Thread
from pyqtgraph.Qt import QtGui, QtCore

from EvolutionSimulation.src.dreamland.Dreamland import Dreamland
from EvolutionSimulation.src.thread.PlantThread import PlantThread
from EvolutionSimulation.src.thread.SheepThread import SheepThread
from EvolutionSimulation.src.thread.TigerThread import TigerThread
from EvolutionSimulation.src.thread.WolfThread import WolfThread
from EvolutionSimulation.src.tool.Recorder import Recorder

TIGER_AMOUNT = 45
WOLF_AMOUNT = 50
SHEEP_AMOUNT = 30
GRASS_AMOUNT = 50

dreamland = Dreamland()
recorder = Recorder(dreamland)

plantThread = PlantThread(GRASS_AMOUNT, dreamland, recorder)
sheepThread = SheepThread(SHEEP_AMOUNT, dreamland, recorder)
wolfThread = WolfThread(WOLF_AMOUNT, dreamland, recorder)
tigerThread = TigerThread(TIGER_AMOUNT, dreamland, recorder)


# class MySignals(QObject):
#     draw = Signal(Dreamland)
#
#
# global_ms = MySignals()



class EvolutionBackground:
    def __init__(self):
        self.__end = False
        self.__pause = False
        self.tiger_amount = 40
        self.wolf_amount = 60
        self.sheep_amount = 80
        self.grass_amount = 50
        self.loop_times = 0

    def terminate(self):
        self.__end = True

    def pause(self):
        self.__pause = True

    def resume(self):
        self.__pause = False

    def run(self):
        Dreamland.startPopulationThread(plantThread)
        Dreamland.startPopulationThread(sheepThread)
        Dreamland.startPopulationThread(wolfThread)
        Dreamland.startPopulationThread(tigerThread)
        start = time.time()

        while not self.__end:
            if not self.__pause:
                time.sleep(1)
                end = time.time()
                print("---Time elapses: " + str(int(end - start)))

                if end - start > 15:
                    Dreamland.stopPopulationThread(plantThread)
                    Dreamland.stopPopulationThread(sheepThread)
                    Dreamland.stopPopulationThread(tigerThread)
                    Dreamland.stopPopulationThread(wolfThread)

                    # global_ms.draw.emit(dreamland)
                    self.loop_times += 1
                    # recorder.writeInfo2File()
                    break
                elif len(wolfThread.group) == 0 and len(tigerThread.group) == 0 and len(sheepThread.group) == 0:
                    Dreamland.stopPopulationThread(plantThread)
                    Dreamland.stopPopulationThread(sheepThread)
                    Dreamland.stopPopulationThread(tigerThread)
                    Dreamland.stopPopulationThread(wolfThread)

                    # global_ms.draw.emit()
                    self.loop_times += 1

                    break


class Evolution:

    def __init__(self):
        self.env = None

        # loader = QUiLoader()
        # loader.registerCustomWidget(pg.PlotWidget)
        self.ui = uic.loadUi("../ui/main.ui")
        self.cur_draw_age = 0

        self.ui.plot_animals.addLegend()
        self.curve_amount_tiger = self.ui.plot_animals.getPlotItem().plot(pen=pg.mkPen('r', width=1), name='Tiger Amount')
        self.curve_amount_wolf = self.ui.plot_animals.getPlotItem().plot(pen=pg.mkPen('g', width=1), name='Wolf Amount')
        self.curve_amount_sheep = self.ui.plot_animals.getPlotItem().plot(pen=pg.mkPen('b', width=1), name='Sheep Amount')
        self.curve_amount_grass = self.ui.plot_grass.getPlotItem().plot(pen=pg.mkPen('y', width=1),name='Grass Amount')

        self.ui.simulate_btn.clicked.connect(self.simulate_clicked)
        # self.ui.pause_btn.clicked.connect(self.pause_clicked)
        # self.ui.plot_custom_btn.clicked.connect(self.plot_custom_clicked)

        #设置时间区间修改事件监听
        self.age_range = int(self.ui.age_range_edit.text())
        self.ui.age_range_edit.editingFinished.connect(self.age_range_edit_finished)

        #后台线程通知更新进化数据
        # global_ms.draw.connect(self.update_env)

        #当前是否在处理模拟暂停或者模拟恢复，因为暂停或恢复需要等待小段时间，期间不要让再次点击
        self.pause_click_handling = False

        self.pause_status = False

        #后台线程运行的逻辑
        self.bg_running_obj = EvolutionBackground()

        self.timer = None
        self.env_thread = None

    def age_range_edit_finished(self):
        self.age_range = int(self.ui.age_range_edit.text())
        print("时间区间编辑完成")


    def simulate_clicked(self):
        if self.timer:
            self.timer.stop()
        if self.env_thread and self.env_thread.is_alive():
            self.bg_running_obj.terminate()
            self.env_thread.join()
        # self.update_params()
        self.env_thread = Thread(target=self.bg_running_obj.run, args=())
        self.env_thread.daemon = True
        self.env_thread.start()
        self.timer = QTimer()
        self.timer.timeout.connect(self.draw_amounts)
        self.timer.start(100)

    def draw_amounts(self):
        self.curve_amount_tiger.setData(range(0, len(tigerThread.num)), tigerThread.num)
        self.curve_amount_wolf.setData(range(0, len(wolfThread.num)), wolfThread.num)
        self.curve_amount_sheep.setData(range(0, len(sheepThread.num)), sheepThread.num)

    # def update_env(self, env):
    #     self.env = env


app = QApplication([])
evolution = Evolution()
evolution.ui.show()
app.exec_()





