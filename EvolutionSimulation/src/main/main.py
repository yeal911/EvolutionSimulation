import os
import sys
# Add project root to path so imports like EvolutionSimulation.src.xxx work
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import time

from PySide6.QtWidgets import (QApplication, QMessageBox, QTabWidget, QWidget,
                               QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox,
                               QTextEdit, QListWidget, QLabel, QSplitter)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Signal, QObject, QTimer
import pyqtgraph as pg
from threading import Thread
from pyqtgraph.Qt import QtGui, QtCore

from EvolutionSimulation.src.dreamland.Dreamland import Dreamland
from EvolutionSimulation.src.thread.PlantThread import PlantThread
from EvolutionSimulation.src.thread.SheepThread import SheepThread
from EvolutionSimulation.src.thread.TigerThread import TigerThread
from EvolutionSimulation.src.thread.WolfThread import WolfThread
from EvolutionSimulation.src.tool.Recorder import Recorder

# New visualization imports
from EvolutionSimulation.src.visualization.WorldMapView import WorldMapView
from EvolutionSimulation.src.visualization.GeneHistogram import GeneHistogramWidget
from EvolutionSimulation.src.visualization.EventLogWidget import EventLogWidget
from EvolutionSimulation.src.visualization.FoodWebGraph import FoodWebWidget
from EvolutionSimulation.src.visualization.FitnessLandscape3D import FitnessLandscape3D
from EvolutionSimulation.src.visualization.StrategyMatrix import StrategyMatrixWidget
from EvolutionSimulation.src.visualization.HeatmapWidget import HeatmapWidget
from EvolutionSimulation.src.visualization.PhylogenyGraph import PhylogenyWidget

TIGER_AMOUNT = 40
WOLF_AMOUNT = 60
SHEEP_AMOUNT = 80
GRASS_AMOUNT = 50

dreamland = Dreamland()
recorder = Recorder(dreamland)

plantThread = PlantThread(GRASS_AMOUNT, dreamland, recorder)
sheepThread = SheepThread(SHEEP_AMOUNT, dreamland, recorder)
wolfThread = WolfThread(WOLF_AMOUNT, dreamland, recorder)
tigerThread = TigerThread(TIGER_AMOUNT, dreamland, recorder)


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
            time.sleep(1)
            end = time.time()
            print("---Time elapses: " + str(int(end - start)))
        Dreamland.stopPopulationThread(plantThread)
        Dreamland.stopPopulationThread(sheepThread)
        Dreamland.stopPopulationThread(tigerThread)
        Dreamland.stopPopulationThread(wolfThread)


class Evolution:

    def __init__(self):
        self.env = None

        loader = QUiLoader()
        loader.registerCustomWidget(pg.PlotWidget)
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ui", "main.ui")
        self.ui = loader.load(ui_path)
        self.cur_draw_age = 0
        # Hook resize FIRST, then resize, so the initial layout is applied immediately
        self._original_resize = self.ui.resizeEvent
        self.ui.resizeEvent = self._on_window_resize
        self.ui.resize(1280, 720)

        # Original plots
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

        # Add new gene attribute curves for new traits
        self._add_new_gene_curves()

        # Add new tabs to existing tab widget
        self._add_enhanced_visualization_tabs()

        # Disable user zoom/pan on original plots; ranges managed manually
        self._setup_plot_interaction()

        # Apply unified visual style for readability
        self._setup_plot_style()

        # Put simple PlotWidget-only tabs into a layout so they auto-fill
        self._setup_tab_layouts()

        self.ui.simulate_btn.clicked.connect(self.simulate_clicked)
        self.ui.pause_btn.clicked.connect(self.pause_clicked)

        self.age_range = int(self.ui.age_range_edit.text())
        self.ui.age_range_edit.editingFinished.connect(self.age_range_edit_finished)

        self.pause_click_handling = False
        self.pause_status = False

        self.bg_running_obj = EvolutionBackground()

        self.timer = None
        self.env_thread = None
        self._frame_counter = 0

    def _add_new_gene_curves(self):
        """Add curves for camouflage, attractiveness, territory tendency."""
        # Tiger
        self.curve_tiger_gene_camouflage = self.ui.plot_tiger_gene.getPlotItem().plot(pen=pg.mkPen((255, 100, 100), width=1), name='Camouflage')
        self.curve_tiger_gene_attractiveness = self.ui.plot_tiger_gene.getPlotItem().plot(pen=pg.mkPen((255, 200, 100), width=1), name='Attractiveness')
        self.curve_tiger_gene_territory = self.ui.plot_tiger_gene.getPlotItem().plot(pen=pg.mkPen((100, 255, 100), width=1), name='Territory')
        # Wolf
        self.curve_wolf_gene_camouflage = self.ui.plot_wolf_gene.getPlotItem().plot(pen=pg.mkPen((255, 100, 100), width=1), name='Camouflage')
        self.curve_wolf_gene_attractiveness = self.ui.plot_wolf_gene.getPlotItem().plot(pen=pg.mkPen((255, 200, 100), width=1), name='Attractiveness')
        self.curve_wolf_gene_territory = self.ui.plot_wolf_gene.getPlotItem().plot(pen=pg.mkPen((100, 255, 100), width=1), name='Territory')
        # Sheep
        self.curve_sheep_gene_camouflage = self.ui.plot_sheep_gene.getPlotItem().plot(pen=pg.mkPen((255, 100, 100), width=1), name='Camouflage')
        self.curve_sheep_gene_attractiveness = self.ui.plot_sheep_gene.getPlotItem().plot(pen=pg.mkPen((255, 200, 100), width=1), name='Attractiveness')
        self.curve_sheep_gene_territory = self.ui.plot_sheep_gene.getPlotItem().plot(pen=pg.mkPen((100, 255, 100), width=1), name='Territory')

    def _add_enhanced_visualization_tabs(self):
        """Add new visualization tabs to the existing QTabWidget."""
        tab_widget = None
        # Check if self.ui itself is a QTabWidget
        if isinstance(self.ui, QTabWidget):
            tab_widget = self.ui
        else:
            # Recursive search
            def find_tab_widget(widget):
                if isinstance(widget, QTabWidget):
                    return widget
                for child in widget.children():
                    if isinstance(child, (QWidget,)):
                        result = find_tab_widget(child)
                        if result:
                            return result
                return None
            tab_widget = find_tab_widget(self.ui)

        if tab_widget is None:
            print("Warning: Could not find QTabWidget in UI")
            return

        # 1. World Map
        self.world_map = WorldMapView(dreamland)
        tab_widget.addTab(self.world_map, "World Map")

        # 2. Heatmap
        self.heatmap = HeatmapWidget(dreamland)
        tab_widget.addTab(self.heatmap, "Density Heatmap")

        # 3. Gene Histograms
        self.gene_hist = GeneHistogramWidget()
        tab_widget.addTab(self.gene_hist, "Gene Distribution")

        # 4. Food Web
        self.food_web = FoodWebWidget()
        tab_widget.addTab(self.food_web, "Food Web")

        # 5. Phylogeny
        self.phylogeny = PhylogenyWidget()
        tab_widget.addTab(self.phylogeny, "Pedigree Tree")

        # 6. Strategy Matrix
        self.strategy_matrix = StrategyMatrixWidget()
        tab_widget.addTab(self.strategy_matrix, "Strategy Matrix")

        # 7. Event Log
        self.event_log = EventLogWidget()
        tab_widget.addTab(self.event_log, "Event Log")

        # 8. 3D Fitness Landscape
        self.fitness_3d = FitnessLandscape3D()
        tab_widget.addTab(self.fitness_3d, "Fitness 3D")

    def age_range_edit_finished(self):
        self.age_range = int(self.ui.age_range_edit.text())
        print("时间区间编辑完成")

    def simulate_clicked(self):
        if self.timer:
            self.timer.stop()
        if self.env_thread and self.env_thread.is_alive():
            self.bg_running_obj.terminate()
            self.env_thread.join()
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

        # Original curves
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

        # New gene attribute curves
        if hasattr(tigerThread, 'avgCamouflage'):
            self.curve_tiger_gene_camouflage.setData(range(0, len(tigerThread.avgCamouflage)), tigerThread.avgCamouflage)
            self.curve_tiger_gene_attractiveness.setData(range(0, len(tigerThread.avgAttractiveness)), tigerThread.avgAttractiveness)
            self.curve_tiger_gene_territory.setData(range(0, len(tigerThread.avgTerritoryTendency)), tigerThread.avgTerritoryTendency)
        if hasattr(wolfThread, 'avgCamouflage'):
            self.curve_wolf_gene_camouflage.setData(range(0, len(wolfThread.avgCamouflage)), wolfThread.avgCamouflage)
            self.curve_wolf_gene_attractiveness.setData(range(0, len(wolfThread.avgAttractiveness)), wolfThread.avgAttractiveness)
            self.curve_wolf_gene_territory.setData(range(0, len(wolfThread.avgTerritoryTendency)), wolfThread.avgTerritoryTendency)
        if hasattr(sheepThread, 'avgCamouflage'):
            self.curve_sheep_gene_camouflage.setData(range(0, len(sheepThread.avgCamouflage)), sheepThread.avgCamouflage)
            self.curve_sheep_gene_attractiveness.setData(range(0, len(sheepThread.avgAttractiveness)), sheepThread.avgAttractiveness)
            self.curve_sheep_gene_territory.setData(range(0, len(sheepThread.avgTerritoryTendency)), sheepThread.avgTerritoryTendency)

        # Update enhanced visualizations
        threads = [tigerThread, wolfThread, sheepThread, plantThread]
        self.world_map.update_map(threads)
        self.heatmap.update_heatmap(threads)

        # Update gene histogram for currently visible species
        self.gene_hist.update_histograms(tigerThread)

        self.food_web.update_graph()
        self.phylogeny.update_tree(threads)
        self.strategy_matrix.update_matrix()
        self.fitness_3d.update_landscape(threads)

        # Update plot ranges: Y-axis dynamically fits current data with padding
        self._update_plot_ranges()

    def _setup_plot_interaction(self):
        """Disable user zoom/pan on original plots; lock Y-min to 0 so origin is always visible."""
        for plot_widget in [self.ui.plot_animals, self.ui.plot_animals_change,
                            self.ui.plot_tiger_gene, self.ui.plot_wolf_gene, self.ui.plot_sheep_gene]:
            if plot_widget is not None:
                plot_item = plot_widget.getPlotItem()
                if plot_item is not None:
                    plot_item.setMouseEnabled(x=False, y=False)
                    plot_item.setMenuEnabled(False)
                    plot_item.hideButtons()
                    # Ensure Y axis never goes below 0 so the origin is always in view
                    plot_item.getViewBox().setLimits(yMin=0)


    def _setup_plot_style(self):
        """Improve readability of all real-time charts."""
        pg.setConfigOptions(antialias=True, foreground='#D6E2F0')

        style_configs = [
            (self.ui.plot_animals, 'Population Size', 'Count'),
            (self.ui.plot_animals_change, 'Population Delta', 'Delta'),
            (self.ui.plot_tiger_gene, 'Tiger Gene Trend', 'Value'),
            (self.ui.plot_wolf_gene, 'Wolf Gene Trend', 'Value'),
            (self.ui.plot_sheep_gene, 'Sheep Gene Trend', 'Value'),
        ]

        for plot_widget, title, y_label in style_configs:
            if plot_widget is None:
                continue
            plot_item = plot_widget.getPlotItem()
            if plot_item is None:
                continue

            plot_item.showGrid(x=True, y=True, alpha=0.25)
            plot_item.setLabel('bottom', 'Time (tick)')
            plot_item.setLabel('left', y_label)
            plot_item.setTitle(f'<span style="font-size:12pt; font-weight:600; color:#EAF2FF;">{title}</span>')
            plot_item.getAxis('bottom').setStyle(tickTextOffset=10, autoExpandTextSpace=True)
            plot_item.getAxis('left').setStyle(autoExpandTextSpace=True)
            plot_item.layout.setContentsMargins(10, 10, 16, 16)

            legend = plot_item.legend
            if legend is not None:
                legend.setBrush(pg.mkBrush(20, 30, 45, 180))
                legend.setPen(pg.mkPen((120, 150, 180), width=1))

    def _setup_tab_layouts(self):
        """Add QVBoxLayout to simple tabs so PlotWidgets auto-fill the tab page.
        Bottom margin is generous so X-axis labels are never clipped."""
        plot_names = ['plot_animals', 'plot_animals_change',
                      'plot_tiger_gene', 'plot_wolf_gene', 'plot_sheep_gene']
        for plot_name in plot_names:
            plot_widget = getattr(self.ui, plot_name, None)
            if plot_widget is None:
                continue
            tab_page = plot_widget.parentWidget()
            if tab_page is None:
                continue
            if tab_page.layout() is not None:
                continue
            layout = QVBoxLayout(tab_page)
            # Large bottom margin specifically for pyqtgraph X-axis tick labels
            layout.setContentsMargins(8, 8, 8, 42)
            layout.setSpacing(0)
            layout.addWidget(plot_widget)

    def _on_window_resize(self, event):
        """Dynamically resize plot_tabs to fill the window.
        PlotWidgets inside tabs auto-fill thanks to QVBoxLayout."""
        if hasattr(self, '_original_resize') and self._original_resize:
            self._original_resize(event)
        w = self.ui.width()
        h = self.ui.height()
        if w < 400 or h < 300:
            return

        # ---- Compact top toolbar (two rows) ----
        y1 = 8
        x = 10
        if hasattr(self.ui, 'simulate_btn'):
            self.ui.simulate_btn.setGeometry(x, y1, 70, 26); x += 78
        if hasattr(self.ui, 'pause_btn'):
            self.ui.pause_btn.setGeometry(x, y1, 70, 26); x += 86

        layout_row1 = [
            ('horizontalLayoutWidget_2', 130),  # Plant
            ('horizontalLayoutWidget_3', 130),  # Sheep
            ('horizontalLayoutWidget_4', 120),  # Wolf
            ('horizontalLayoutWidget_5', 120),  # Tiger
        ]
        for name, lw_w in layout_row1:
            lw = getattr(self.ui, name, None)
            if lw:
                lw.setGeometry(x, y1, lw_w, 26)
                x += lw_w + 6

        y2 = 38
        x2 = 10
        lw = getattr(self.ui, 'horizontalLayoutWidget', None)
        if lw:
            lw.setGeometry(x2, y2, 140, 22); x2 += 150
        lw = getattr(self.ui, 'horizontalLayoutWidget_10', None)
        if lw:
            lw.setGeometry(x2, y2, 140, 22)

        # ---- plot_tabs fills everything below the toolbar ----
        tabs_y = 68
        tabs = getattr(self.ui, 'plot_tabs', None)
        if tabs is not None:
            tabs.setGeometry(10, tabs_y, w - 20, h - tabs_y - 14)

    def _update_plot_ranges(self):
        """Let pyqtgraph auto-range handle everything; it knows best how to keep axes visible.
        We only ensure Y never drops below 0 (already set via setLimits in _setup_plot_interaction)."""
        self._frame_counter += 1
        if self._frame_counter % 10 == 0:
            for plot_widget in [self.ui.plot_animals, self.ui.plot_animals_change,
                                self.ui.plot_tiger_gene, self.ui.plot_wolf_gene, self.ui.plot_sheep_gene]:
                if plot_widget is not None:
                    plot_item = plot_widget.getPlotItem()
                    if plot_item is not None:
                        plot_item.autoRange()


app = QApplication([])
evolution = Evolution()
# Show at default 1280x720; user can resize/maximize manually if screen permits
evolution.ui.show()
app.exec_()
