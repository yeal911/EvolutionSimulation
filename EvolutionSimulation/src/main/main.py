import os
import sys
import time


from PySide2.QtWidgets import QApplication, QMessageBox
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

TIGER_AMOUNT = 450
WOLF_AMOUNT = 500
SHEEP_AMOUNT = 800
GRASS_AMOUNT = 500

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

        while not self.__pause:
            # if not self.__pause:
            time.sleep(1)
            end = time.time()
            print("---Time elapses: " + str(int(end - start)))

            # if end - start > 10:
            #     Dreamland.stopPopulationThread(plantThread)
            #     Dreamland.stopPopulationThread(sheepThread)
            #     Dreamland.stopPopulationThread(tigerThread)
            #     Dreamland.stopPopulationThread(wolfThread)
            #
            #     break
            # elif len(wolfThread.group) == 0 and len(tigerThread.group) == 0 and len(sheepThread.group) == 0:
            #     Dreamland.stopPopulationThread(plantThread)
            #     Dreamland.stopPopulationThread(sheepThread)
            #     Dreamland.stopPopulationThread(tigerThread)
            #     Dreamland.stopPopulationThread(wolfThread)
            #
            #     break
        Dreamland.stopPopulationThread(plantThread)
        Dreamland.stopPopulationThread(sheepThread)
        Dreamland.stopPopulationThread(tigerThread)
        Dreamland.stopPopulationThread(wolfThread)


class Evolution:

    def __init__(self):
        self.env = None

        loader = QUiLoader()
        loader.registerCustomWidget(pg.PlotWidget)
        self.ui = loader.load("E:/Python/EvolutionSimulation/src/ui/main.ui")
        self.cur_draw_age = 0

        self.ui.plot_animals.addLegend()
        self.curve_amount_tiger = self.ui.plot_animals.getPlotItem().plot(pen=pg.mkPen('r', width=1), name='Tiger Amount')
        self.curve_amount_wolf = self.ui.plot_animals.getPlotItem().plot(pen=pg.mkPen('g', width=1), name='Wolf Amount')
        self.curve_amount_sheep = self.ui.plot_animals.getPlotItem().plot(pen=pg.mkPen('b', width=1), name='Sheep Amount')
        self.curve_amount_grass = self.ui.plot_animals.getPlotItem().plot(pen=pg.mkPen('y', width=1), name='Grass Amount')


        self.ui.plot_animals_change.addLegend()
        self.curve_add_tiger = self.ui.plot_animals_change.getPlotItem().plot(pen=pg.mkPen('r', width=1), name='Tiger Born')
        self.curve_sub_tiger = self.ui.plot_animals_change.getPlotItem().plot(pen=pg.mkPen('g', width=1), name='Tiger Dead')
        self.curve_add_wolf = self.ui.plot_animals_change.getPlotItem().plot(pen=pg.mkPen('b', width=1), name='Wolf Born')
        self.curve_sub_wolf = self.ui.plot_animals_change.getPlotItem().plot(pen=pg.mkPen('c', width=1), name='Wolf Dead')
        self.curve_add_sheep = self.ui.plot_animals_change.getPlotItem().plot(pen=pg.mkPen('m', width=1), name='Sheep Born')
        self.curve_sub_sheep = self.ui.plot_animals_change.getPlotItem().plot(pen=pg.mkPen('y', width=1), name='Sheep Dead')
        self.curve_sub_grass = self.ui.plot_animals_change.getPlotItem().plot(pen=pg.mkPen('d', width=1), name='Grass Cost')


        self.ui.plot_tiger_gene.addLegend()
        self.curve_tiger_gene_hungry_level = self.ui.plot_tiger_gene.getPlotItem().plot(pen=pg.mkPen('r', width=1), name='Hungry Level')
        self.curve_tiger_gene_lifespan = self.ui.plot_tiger_gene.getPlotItem().plot(pen=pg.mkPen('y', width=1), name='LifeSpan')
        self.curve_tiger_gene_fightCapability = self.ui.plot_tiger_gene.getPlotItem().plot(pen=pg.mkPen('g', width=1), name='fightCapability')
        self.curve_tiger_gene_age = self.ui.plot_tiger_gene.getPlotItem().plot(pen=pg.mkPen('w', width=1), name='Age')
        self.curve_tiger_gene_attack = self.ui.plot_tiger_gene.getPlotItem().plot(pen=pg.mkPen('c', width=1), name='AttackPossibility')
        self.curve_tiger_gene_defend = self.ui.plot_tiger_gene.getPlotItem().plot(pen=pg.mkPen('m', width=1), name='DefendPossibility')
        self.curve_tiger_gene_breed = self.ui.plot_tiger_gene.getPlotItem().plot(pen=pg.mkPen('b', width=1), name='BreedingTimes')

        self.ui.plot_wolf_gene.addLegend()
        self.curve_wolf_gene_hungry_level = self.ui.plot_wolf_gene.getPlotItem().plot(pen=pg.mkPen('r', width=1), name='Hungry Level')
        self.curve_wolf_gene_lifespan = self.ui.plot_wolf_gene.getPlotItem().plot(pen=pg.mkPen('y', width=1), name='LifeSpan')
        self.curve_wolf_gene_fightCapability = self.ui.plot_wolf_gene.getPlotItem().plot(pen=pg.mkPen('g', width=1), name='fightCapability')
        self.curve_wolf_gene_age = self.ui.plot_wolf_gene.getPlotItem().plot(pen=pg.mkPen('w', width=1), name='Age')
        self.curve_wolf_gene_attack = self.ui.plot_wolf_gene.getPlotItem().plot(pen=pg.mkPen('c', width=1), name='AttackPossibility')
        self.curve_wolf_gene_defend = self.ui.plot_wolf_gene.getPlotItem().plot(pen=pg.mkPen('m', width=1), name='DefendPossibility')
        self.curve_wolf_gene_breed = self.ui.plot_wolf_gene.getPlotItem().plot(pen=pg.mkPen('b', width=1), name='BreedingTimes')


        self.ui.plot_sheep_gene.addLegend()
        self.curve_sheep_gene_hungry_level = self.ui.plot_sheep_gene.getPlotItem().plot(pen=pg.mkPen('r', width=1), name='Hungry Level')
        self.curve_sheep_gene_lifespan = self.ui.plot_sheep_gene.getPlotItem().plot(pen=pg.mkPen('y', width=1), name='LifeSpan')
        self.curve_sheep_gene_fightCapability = self.ui.plot_sheep_gene.getPlotItem().plot(pen=pg.mkPen('g', width=1), name='fightCapability')
        self.curve_sheep_gene_age = self.ui.plot_sheep_gene.getPlotItem().plot(pen=pg.mkPen('w', width=1), name='Age')
        self.curve_sheep_gene_attack = self.ui.plot_sheep_gene.getPlotItem().plot(pen=pg.mkPen('c', width=1), name='AttackPossibility')
        self.curve_sheep_gene_defend = self.ui.plot_sheep_gene.getPlotItem().plot(pen=pg.mkPen('m', width=1), name='DefendPossibility')
        self.curve_sheep_gene_breed = self.ui.plot_sheep_gene.getPlotItem().plot(pen=pg.mkPen('b', width=1), name='BreedingTimes')


        self.ui.simulate_btn.clicked.connect(self.simulate_clicked)
        self.ui.pause_btn.clicked.connect(self.pause_clicked)

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

    def pause_clicked(self):
        if self.pause_status:
            print("点击了恢复")
            self.ui.pause_btn.setEnabled(False)
            print("执行恢复")
            self.bg_running_obj.resume()
            print("恢复成功")
            self.pause_status = False
            self.ui.pause_btn.setEnabled(True)
            self.ui.pause_btn.setText("Pause")
        else:
            print("点击了暂停")
            self.ui.pause_btn.setEnabled(False)
            print("执行暂停")
            self.bg_running_obj.pause()
            print("暂停成功")
            self.pause_status = True
            self.ui.pause_btn.setEnabled(True)
            self.ui.pause_btn.setText("Continue")

    def draw_amounts(self):
        self.ui.loop_count_label.setText(str(len(tigerThread.num)))

        self.curve_amount_tiger.setData(range(0, len(tigerThread.num)), tigerThread.num)
        self.curve_amount_wolf.setData(range(0, len(wolfThread.num)), wolfThread.num)
        self.curve_amount_sheep.setData(range(0, len(sheepThread.num)), sheepThread.num)
        self.curve_amount_grass.setData(range(0, len(plantThread.num)), plantThread.num)

        self.curve_add_tiger.setData(range(0, len(tigerThread.newBronNum)), tigerThread.newBronNum)
        self.curve_sub_tiger.setData(range(0, len(tigerThread.newDeathNum)), tigerThread.newDeathNum)

        self.curve_add_wolf.setData(range(0, len(wolfThread.newBronNum)), wolfThread.newBronNum)
        self.curve_sub_wolf.setData(range(0, len(wolfThread.newDeathNum)), wolfThread.newDeathNum)

        self.curve_add_sheep.setData(range(0, len(sheepThread.newBronNum)), sheepThread.newBronNum)
        self.curve_sub_sheep.setData(range(0, len(sheepThread.newDeathNum)), sheepThread.newDeathNum)

        # self.curve_add_grass.setData()
        self.curve_sub_grass.setData(range(0, len(plantThread.newDeathNum)), plantThread.newDeathNum)

        self.curve_tiger_gene_hungry_level.setData(range(0, len(tigerThread.avgHungryLevel)), tigerThread.avgHungryLevel)
        self.curve_tiger_gene_lifespan.setData(range(0, len(tigerThread.avgLifespan)), tigerThread.avgLifespan)
        self.curve_tiger_gene_fightCapability.setData(range(0, len(tigerThread.avgFightCapability)), tigerThread.avgFightCapability)
        self.curve_tiger_gene_age.setData(range(0, len(tigerThread.avgAge)), tigerThread.avgAge)
        self.curve_tiger_gene_attack.setData(range(0, len(tigerThread.avgAttackPossibility)), tigerThread.avgAttackPossibility)
        self.curve_tiger_gene_defend.setData(range(0, len(tigerThread.avgDefendPossibility)), tigerThread.avgDefendPossibility)
        self.curve_tiger_gene_breed.setData(range(0, len(tigerThread.avgTotalBreedingTimes)), tigerThread.avgTotalBreedingTimes)


        self.curve_wolf_gene_hungry_level.setData(range(0, len(wolfThread.avgHungryLevel)), wolfThread.avgHungryLevel)
        self.curve_wolf_gene_lifespan.setData(range(0, len(wolfThread.avgLifespan)), wolfThread.avgLifespan)
        self.curve_wolf_gene_fightCapability.setData(range(0, len(wolfThread.avgFightCapability)), wolfThread.avgFightCapability)
        self.curve_wolf_gene_age.setData(range(0, len(wolfThread.avgAge)), wolfThread.avgAge)
        self.curve_wolf_gene_attack.setData(range(0, len(wolfThread.avgAttackPossibility)), wolfThread.avgAttackPossibility)
        self.curve_wolf_gene_defend.setData(range(0, len(wolfThread.avgDefendPossibility)), wolfThread.avgDefendPossibility)
        self.curve_wolf_gene_breed.setData(range(0, len(wolfThread.avgTotalBreedingTimes)), wolfThread.avgTotalBreedingTimes)


        self.curve_sheep_gene_hungry_level.setData(range(0, len(sheepThread.avgHungryLevel)), sheepThread.avgHungryLevel)
        self.curve_sheep_gene_lifespan.setData(range(0, len(sheepThread.avgLifespan)), sheepThread.avgLifespan)
        self.curve_sheep_gene_fightCapability.setData(range(0, len(sheepThread.avgFightCapability)), sheepThread.avgFightCapability)
        self.curve_sheep_gene_age.setData(range(0, len(sheepThread.avgAge)), sheepThread.avgAge)
        self.curve_sheep_gene_attack.setData(range(0, len(sheepThread.avgAttackPossibility)), sheepThread.avgAttackPossibility)
        self.curve_sheep_gene_defend.setData(range(0, len(sheepThread.avgDefendPossibility)), sheepThread.avgDefendPossibility)
        self.curve_sheep_gene_breed.setData(range(0, len(sheepThread.avgTotalBreedingTimes)), sheepThread.avgTotalBreedingTimes)


app = QApplication([])
evolution = Evolution()
evolution.ui.show()
app.exec_()





