from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QCheckBox, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from EvolutionSimulation.src.event.EventLogger import EventLogger


class EventLogWidget(QWidget):
    """Real-time event log display with filtering."""

    TYPE_COLORS = {
        "Fight": QColor(255, 100, 100),
        "Breed": QColor(100, 255, 100),
        "Altruism": QColor(100, 200, 255),
        "KinSelection": QColor(200, 150, 255),
        "SexualSelection": QColor(255, 150, 200),
        "Nest": QColor(160, 100, 50),
        "Territory": QColor(255, 200, 50),
        "Parasite": QColor(150, 50, 150),
        "PD": QColor(50, 150, 100),
        "Greenbeard": QColor(50, 200, 50),
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.filter_layout = QHBoxLayout()
        self.type_checks = {}
        for event_type in self.TYPE_COLORS.keys():
            cb = QCheckBox(event_type)
            cb.setChecked(True)
            self.type_checks[event_type] = cb
            self.filter_layout.addWidget(cb)
        self.filter_layout.addStretch()
        self.layout.addLayout(self.filter_layout)

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        EventLogger().register_listener(self.on_event)

    def on_event(self, entry):
        event_type = entry.get("type", "")
        if event_type not in self.type_checks or not self.type_checks[event_type].isChecked():
            return
        text = f"[{entry['time']}] [{event_type}] {entry['message']}"
        item = QListWidgetItem(text)
        color = self.TYPE_COLORS.get(event_type, QColor(200, 200, 200))
        item.setForeground(color)
        self.list_widget.addItem(item)
        self.list_widget.scrollToBottom()
        # Limit items
        while self.list_widget.count() > 200:
            self.list_widget.takeItem(0)

    def clear_log(self):
        self.list_widget.clear()
