from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QCheckBox, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from EvolutionSimulation.src.event.EventLogger import EventLogger


class EventLogWidget(QWidget):
    """Real-time event log display with filtering."""

    TYPE_COLORS = {
        "Fight": QColor(255, 107, 107),
        "Breed": QColor(78, 203, 113),
        "Altruism": QColor(100, 200, 255),
        "KinSelection": QColor(200, 150, 255),
        "SexualSelection": QColor(255, 150, 200),
        "Nest": QColor(200, 150, 80),
        "Territory": QColor(255, 200, 50),
        "Parasite": QColor(180, 80, 180),
        "PD": QColor(80, 200, 150),
        "Greenbeard": QColor(80, 220, 80),
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(4)

        self.filter_layout = QHBoxLayout()
        self.type_checks = {}
        for event_type in self.TYPE_COLORS.keys():
            cb = QCheckBox(event_type)
            cb.setChecked(True)
            cb.setStyleSheet("color: #C8D6E5; font-size: 11px;")
            self.type_checks[event_type] = cb
            self.filter_layout.addWidget(cb)
        self.filter_layout.addStretch()
        self.layout.addLayout(self.filter_layout)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #0F1923;
                color: #C8D6E5;
                font-family: Consolas, monospace;
                font-size: 11px;
                border: 1px solid #2D3748;
                border-radius: 4px;
            }
            QListWidget::item {
                padding: 2px 4px;
                border-bottom: 1px solid #1A2332;
            }
        """)
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
        while self.list_widget.count() > 200:
            self.list_widget.takeItem(0)

    def clear_log(self):
        self.list_widget.clear()
