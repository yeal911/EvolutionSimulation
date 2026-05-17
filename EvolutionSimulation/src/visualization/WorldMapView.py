from PySide6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsRectItem,
                               QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout, QLabel)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush, QPen


class _LegendItem(QWidget):
    """Single row in the legend: color swatch + label + optional count."""
    def __init__(self, color, text, count=None, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 1, 2, 1)
        layout.setSpacing(4)

        swatch = QLabel()
        swatch.setFixedSize(12, 12)
        swatch.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #555555; border-radius: 2px;")
        layout.addWidget(swatch)

        lbl = QLabel(text)
        lbl.setStyleSheet("color: #C8D6E5; font-size: 11px;")
        layout.addWidget(lbl)

        self.count_label = None
        if count is not None:
            self.count_label = QLabel(str(count))
            self.count_label.setStyleSheet("color: #FFD93D; font-size: 11px; font-weight: bold;")
            layout.addWidget(self.count_label)
        layout.addStretch()

    def set_count(self, count):
        if self.count_label:
            self.count_label.setText(str(count))


class WorldMapView(QGraphicsView):
    """2D spatial world map rendering individuals as colored dots."""

    COLORS = {
        "Tiger": QColor(255, 107, 107),
        "Wolf": QColor(148, 163, 184),
        "Sheep": QColor(74, 158, 255),
        "Plant": QColor(78, 203, 113),
    }

    TERRAIN_COLORS = {
        0: QColor(45, 55, 72),    # Plain (dark)
        1: QColor(30, 70, 50),    # Forest
        2: QColor(80, 65, 40),    # Desert
        3: QColor(30, 55, 90),    # Water
        4: QColor(60, 60, 65),    # Mountain
    }

    def __init__(self, dreamland, parent=None):
        super().__init__(parent)
        self.dreamland = dreamland
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(200, 200)
        self.setDragMode(QGraphicsView.NoDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scene.setSceneRect(0, 0, 700, 350)
        self.showTrails = True
        self._terrain_items = []
        self._draw_terrain()
        self._dynamic_items = []
        self._build_legend_overlay()
        # Dark viewport background
        self.setStyleSheet("background-color: #0F1923;")

    def _build_legend_overlay(self):
        """Create a floating legend widget on the right side of the viewport."""
        self._legend_panel = QWidget(self)
        self._legend_panel.setStyleSheet("background-color: rgba(15, 25, 35, 210); border-radius: 6px;")
        vbox = QVBoxLayout(self._legend_panel)
        vbox.setContentsMargins(8, 6, 8, 6)
        vbox.setSpacing(2)

        # Species entries with population count labels
        self._species_legend_items = {}
        species_entries = [
            ("Tiger", self.COLORS["Tiger"]),
            ("Wolf", self.COLORS["Wolf"]),
            ("Sheep", self.COLORS["Sheep"]),
            ("Plant", self.COLORS["Plant"]),
        ]
        for name, color in species_entries:
            item = _LegendItem(color, name, count=0, parent=self._legend_panel)
            self._species_legend_items[name] = item
            vbox.addWidget(item)

        # Separator
        sep = QLabel("─" * 14)
        sep.setStyleSheet("color: #4A5568; font-size: 9px;")
        vbox.addWidget(sep)

        # Static entries (terrain types, etc.)
        static_entries = [
            (QColor(139, 69, 19), "Nest"),
            (self.TERRAIN_COLORS[0], "Plain"),
            (self.TERRAIN_COLORS[1], "Forest"),
            (self.TERRAIN_COLORS[2], "Desert"),
            (self.TERRAIN_COLORS[3], "Water"),
            (self.TERRAIN_COLORS[4], "Mountain"),
        ]
        for color, text in static_entries:
            vbox.addWidget(_LegendItem(color, text, parent=self._legend_panel))

        self._legend_panel.setFixedSize(140, 280)
        self._legend_panel.move(self.viewport().width() - 148, 8)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._apply_transform()
        if hasattr(self, '_legend_panel'):
            self._legend_panel.move(self.viewport().width() - 148, 8)

    def _draw_terrain(self):
        slot_size = 10
        for slot_code, terrain_type in self.dreamland.terrainMap.items():
            parts = slot_code.split("A")
            x = int(parts[0]) - slot_size
            y = int(parts[1]) - slot_size
            rect = QGraphicsRectItem(x, y, slot_size, slot_size)
            color = self.TERRAIN_COLORS.get(terrain_type, QColor(40, 40, 45))
            rect.setPen(QPen(Qt.NoPen))
            rect.setBrush(QBrush(color))
            self.scene.addItem(rect)
            self._terrain_items.append(rect)

    def _clear_dynamic_items(self):
        for item in self._dynamic_items:
            self.scene.removeItem(item)
        self._dynamic_items.clear()

    def update_map(self, threads):
        self._clear_dynamic_items()

        # Update population counts in legend (only count alive individuals)
        for thread in threads:
            species = thread.THREAD_NAME.replace("Thread", "")
            if species in self._species_legend_items:
                alive_count = sum(1 for ind in thread.group if getattr(ind, 'lifeStatus', 'Dead') == 'Alive')
                self._species_legend_items[species].set_count(alive_count)

        for slot_code, nests in self.dreamland.nestMap.items():
            for nest in nests:
                parts = slot_code.split("A")
                x = int(parts[0]) - 5
                y = int(parts[1]) - 5
                ellipse = QGraphicsEllipseItem(x - 4, y - 4, 8, 8)
                ellipse.setBrush(QBrush(QColor(139, 69, 19)))
                ellipse.setPen(QPen(Qt.NoPen))
                self.scene.addItem(ellipse)
                self._dynamic_items.append(ellipse)

        for thread in threads:
            species = thread.THREAD_NAME.replace("Thread", "")
            base_color = self.COLORS.get(species, QColor(200, 200, 200))
            # Snapshot group list to avoid threading race condition
            group_snapshot = list(thread.group)
            for ind in group_snapshot:
                if getattr(ind, 'lifeStatus', 'Dead') != 'Alive':
                    continue
                x = ind.coordinateX
                y = ind.coordinateY
                size = min(14, max(5, ind.fightCapability / 8))
                ellipse = QGraphicsEllipseItem(x - size/2, y - size/2, size, size)
                opacity = max(0.6, 1.0 - ind.age / (ind.lifespan + 1))
                color = QColor(base_color)
                color.setAlphaF(opacity)
                ellipse.setBrush(QBrush(color))
                ellipse.setPen(QPen(QColor(255, 255, 255, 100), 0.8))
                self.scene.addItem(ellipse)
                self._dynamic_items.append(ellipse)

        if self.showTrails:
            for thread in threads:
                if thread.THREAD_TYPE != "Animal":
                    continue
                base_color = self.COLORS.get(thread.THREAD_NAME.replace("Thread", ""), QColor(200, 200, 200))
                group_snapshot = list(thread.group)
                for ind in group_snapshot:
                    hist = list(ind.moveHistory.items())
                    if len(hist) < 2:
                        continue
                    recent = hist[-10:]
                    points = []
                    for cycle, loc in recent:
                        parts = loc.split("|")
                        px = int(parts[0])
                        py = int(parts[1].split(",")[0])
                        points.append((px, py))
                    for i in range(1, len(points)):
                        line = self.scene.addLine(points[i-1][0], points[i-1][1],
                                                   points[i][0], points[i][1],
                                                   QPen(QColor(base_color.red(), base_color.green(),
                                                               base_color.blue(), 80), 1.5))
                        self._dynamic_items.append(line)

        self._apply_transform()

    def _apply_transform(self):
        vw = self.viewport().width()
        vh = self.viewport().height()
        if vw <= 0 or vh <= 0:
            return
        scale = min(vw / 700.0, vh / 350.0)
        self.resetTransform()
        self.scale(scale, scale)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    def set_show_trails(self, show):
        self.showTrails = show

    def wheelEvent(self, event):
        event.ignore()

    def mousePressEvent(self, event):
        event.ignore()

    def mouseMoveEvent(self, event):
        event.ignore()

    def mouseReleaseEvent(self, event):
        event.ignore()
