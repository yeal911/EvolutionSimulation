import pyqtgraph as pg
from PySide6.QtWidgets import QVBoxLayout, QWidget


class GeneHistogramWidget(QWidget):
    """Histogram showing gene frequency distribution per species."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.plots = []
        for i in range(10):
            plot = pg.PlotWidget(title=f"Gene Bit {i}")
            plot.setMaximumHeight(120)
            self.layout.addWidget(plot)
            self.plots.append(plot)
        self.bars = [None] * 10

    def update_histograms(self, thread):
        if not thread.group:
            return
        for bit in range(10):
            values = [ind.gene.geneDigits[bit] for ind in thread.group]
            # Bin into 10 bins (0-9, 10-19, ..., 90-99)
            y = [0] * 10
            for v in values:
                y[min(v // 10, 9)] += 1
            x = list(range(10))
            plot = self.plots[bit]
            plot.clear()
            bar = pg.BarGraphItem(x=x, height=y, width=0.8, brush='b')
            plot.addItem(bar)
