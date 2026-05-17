import pyqtgraph as pg
from PySide6.QtWidgets import QVBoxLayout, QWidget


class GeneHistogramWidget(QWidget):
    """Histogram showing gene frequency distribution per species."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(2)
        self.plots = []
        for i in range(10):
            plot = pg.PlotWidget(title=f'<span style="font-size:10pt; color:#C8D6E5;">Gene Bit {i}</span>')
            plot.setMaximumHeight(110)
            plot.setMinimumHeight(60)
            pi = plot.getPlotItem()
            pi.layout.setContentsMargins(8, 6, 16, 14)
            pi.getAxis('bottom').setHeight(36)
            pi.getAxis('left').setWidth(48)
            pi.getViewBox().setBackgroundColor('#0F1923')
            pi.showGrid(x=False, y=True, alpha=0.12)
            self.layout.addWidget(plot)
            self.plots.append(plot)
        self.bars = [None] * 10

    def update_histograms(self, thread):
        if not thread.group:
            return
        for bit in range(10):
            values = [ind.gene.geneDigits[bit] for ind in thread.group]
            y = [0] * 10
            for v in values:
                y[min(v // 10, 9)] += 1
            x = list(range(10))
            plot = self.plots[bit]
            plot.clear()
            bar = pg.BarGraphItem(x=x, height=y, width=0.8, brush='#4A9EFF')
            plot.addItem(bar)
