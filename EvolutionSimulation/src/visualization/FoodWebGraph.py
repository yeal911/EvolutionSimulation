import pyqtgraph as pg
from PySide6.QtWidgets import QVBoxLayout, QWidget


class FoodWebWidget(QWidget):
    """Food web network graph showing predation relationships."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.plot = pg.PlotWidget(title="Food Web Network")
        self.layout.addWidget(self.plot)
        self.plot.setXRange(-2, 4)
        self.plot.setYRange(-2, 4)
        self.plot.hideAxis('left')
        self.plot.hideAxis('bottom')
        self.predation_counts = {
            "Tiger->Wolf": 0, "Tiger->Sheep": 0,
            "Wolf->Sheep": 0, "Wolf->Wolf": 0,
            "Sheep->Plant": 0,
        }

    def record_fight(self, attacker_species, defender_species):
        key = f"{attacker_species}->{defender_species}"
        if key in self.predation_counts:
            self.predation_counts[key] += 1

    def update_graph(self):
        self.plot.clear()
        # Node positions
        nodes = {
            "Plant": (0, -2),
            "Sheep": (0, 0),
            "Wolf": (-1.5, 2),
            "Tiger": (1.5, 2),
        }
        colors = {"Plant": 'g', "Sheep": 'b', "Wolf": 'gray', "Tiger": 'r'}
        for name, (x, y) in nodes.items():
            scatter = pg.ScatterPlotItem(x=[x], y=[y], pen=pg.mkPen(colors[name], width=2),
                                         brush=pg.mkBrush(colors[name]), size=30)
            self.plot.addItem(scatter)
            text = pg.TextItem(name, anchor=(0.5, 1.2))
            text.setPos(x, y)
            self.plot.addItem(text)

        # Edges with thickness based on predation count
        edges = [
            ("Sheep", "Plant", self.predation_counts["Sheep->Plant"]),
            ("Wolf", "Sheep", self.predation_counts["Wolf->Sheep"]),
            ("Wolf", "Wolf", self.predation_counts["Wolf->Wolf"]),
            ("Tiger", "Sheep", self.predation_counts["Tiger->Sheep"]),
            ("Tiger", "Wolf", self.predation_counts["Tiger->Wolf"]),
        ]
        for src, dst, count in edges:
            if count > 0:
                x1, y1 = nodes[src]
                x2, y2 = nodes[dst]
                pen = pg.mkPen('w', width=min(10, max(1, count / 5)))
                self.plot.plot([x1, x2], [y1, y2], pen=pen)
