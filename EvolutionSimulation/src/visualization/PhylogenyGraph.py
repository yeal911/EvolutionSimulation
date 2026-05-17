import pyqtgraph as pg
from PySide6.QtWidgets import QVBoxLayout, QWidget


class PhylogenyWidget(QWidget):
    """Simple pedigree tree for tracing ancestors of a selected individual."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.plot = pg.PlotWidget(title="Pedigree Tree (Last 3 Generations)")
        self.layout.addWidget(self.plot)
        self.plot.hideAxis('left')
        self.plot.hideAxis('bottom')
        self.plot.setXRange(-5, 5)
        self.plot.setYRange(-1, 5)

    def update_tree(self, threads):
        self.plot.clear()
        # Find the individual with highest generation
        target = None
        max_gen = 0
        for thread in threads:
            if thread.THREAD_TYPE == "Animal":
                for ind in thread.group:
                    if ind.generation > max_gen:
                        max_gen = ind.generation
                        target = ind
        if target is None or max_gen < 2:
            text = pg.TextItem("No multi-generation pedigree yet", anchor=(0.5, 0.5))
            text.setPos(0, 2)
            self.plot.addItem(text)
            return

        # Draw target at top
        scatter = pg.ScatterPlotItem(x=[0], y=[max_gen], pen=pg.mkPen('r', width=2),
                                     brush=pg.mkBrush('r'), size=20)
        self.plot.addItem(scatter)
        text = pg.TextItem(target.name, anchor=(0.5, -0.5))
        text.setPos(0, max_gen)
        self.plot.addItem(text)

        # Try to trace parents from parents string
        parents = target.parents.split("/") if target.parents else []
        if len(parents) >= 2:
            for idx, pname in enumerate(parents[:2]):
                px = -2 if idx == 0 else 2
                py = max_gen - 1
                pen = pg.mkPen('b', width=2)
                self.plot.plot([0, px], [max_gen, py], pen=pen)
                scatter = pg.ScatterPlotItem(x=[px], y=[py], pen=pen, brush=pg.mkBrush('b'), size=15)
                self.plot.addItem(scatter)
                ptext = pg.TextItem(pname, anchor=(0.5, -0.5))
                ptext.setPos(px, py)
                self.plot.addItem(ptext)
