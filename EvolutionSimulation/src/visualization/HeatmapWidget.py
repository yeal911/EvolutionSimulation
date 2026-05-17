import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QVBoxLayout, QWidget
from EvolutionSimulation.src.dreamland.Dreamland import Dreamland


class HeatmapWidget(QWidget):
    """Population density heatmap over the world grid."""

    def __init__(self, dreamland, parent=None):
        super().__init__(parent)
        self.dreamland = dreamland
        self.layout = QVBoxLayout(self)
        self.plot = pg.PlotWidget(
            title='<span style="font-size:13pt; font-weight:600; color:#EAF2FF;">Population Density Heatmap</span>')
        self.layout.addWidget(self.plot)
        self.img = pg.ImageItem()
        self.plot.addItem(self.img)
        self.plot.setXRange(0, 50)
        self.plot.setYRange(0, 50)
        self.grid_x = Dreamland.SIZE_X // 10
        self.grid_y = Dreamland.SIZE_Y // 10
        # Styling
        pi = self.plot.getPlotItem()
        pi.layout.setContentsMargins(16, 14, 40, 36)
        pi.getAxis('bottom').setHeight(56)
        pi.getAxis('left').setWidth(68)
        pi.getViewBox().setBackgroundColor('#0F1923')
        pi.showGrid(x=False, y=False)

    def update_heatmap(self, threads):
        grid = np.zeros((self.grid_y, self.grid_x))
        for thread in threads:
            if thread.THREAD_TYPE == "Animal":
                for ind in thread.group:
                    gx = min(ind.coordinateX // 10, self.grid_x - 1)
                    gy = min(ind.coordinateY // 10, self.grid_y - 1)
                    grid[int(gy), int(gx)] += 1
        if grid.max() > 0:
            grid = grid / grid.max()
        self.img.setImage(grid)
        self.img.setRect(0, 0, self.grid_x, self.grid_y)
