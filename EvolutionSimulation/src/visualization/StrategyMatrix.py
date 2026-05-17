import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QVBoxLayout, QWidget


class StrategyMatrixWidget(QWidget):
    """Strategy coexistence matrix heatmap for Prisoner's Dilemma."""

    STRATEGY_NAMES = ["AlwaysCoop", "AlwaysDefect", "TitForTat", "Random"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.plot = pg.PlotWidget(
            title='<span style="font-size:13pt; font-weight:600; color:#EAF2FF;">Strategy Payoff Matrix</span>')
        self.layout.addWidget(self.plot)
        self.plot.hideAxis('left')
        self.plot.hideAxis('bottom')
        pi = self.plot.getPlotItem()
        pi.getViewBox().setBackgroundColor('#0F1923')
        pi.layout.setContentsMargins(12, 12, 12, 12)
        self.img = pg.ImageItem()
        self.plot.addItem(self.img)
        self.payoff_matrix = np.zeros((4, 4))
        self.text_items = []

    def record_payoff(self, strategy_a, strategy_b, payoff_a):
        self.payoff_matrix[strategy_a, strategy_b] += payoff_a

    def update_matrix(self):
        mat = self.payoff_matrix.copy()
        max_val = mat.max() if mat.max() > 0 else 1
        mat = mat / max_val
        self.img.setImage(mat)
        self.img.setRect(0, 0, 4, 4)

        for t in self.text_items:
            self.plot.removeItem(t)
        self.text_items = []

        for i in range(4):
            for j in range(4):
                text = pg.TextItem(f"{self.payoff_matrix[i, j]:.0f}", color='#E2E8F0', anchor=(0.5, 0.5))
                text.setPos(j + 0.5, i + 0.5)
                self.plot.addItem(text)
                self.text_items.append(text)
                if i == 0:
                    top = pg.TextItem(self.STRATEGY_NAMES[j], color='#C8D6E5', anchor=(0.5, 1.0))
                    top.setPos(j + 0.5, 4.1)
                    self.plot.addItem(top)
                    self.text_items.append(top)
                if j == 0:
                    left = pg.TextItem(self.STRATEGY_NAMES[i], color='#C8D6E5', anchor=(1.0, 0.5))
                    left.setPos(-0.1, i + 0.5)
                    self.plot.addItem(left)
                    self.text_items.append(left)
