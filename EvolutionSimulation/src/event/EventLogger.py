import time
from collections import deque


class EventLogger:
    """Global event logger for real-time event log visualization."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.events = deque(maxlen=500)
            cls._instance.listeners = []
        return cls._instance

    def log(self, event_type, message):
        """Log an event with timestamp."""
        entry = {
            "time": time.strftime("%H:%M:%S", time.localtime()),
            "type": event_type,
            "message": message
        }
        self.events.append(entry)
        for listener in self.listeners:
            try:
                listener(entry)
            except Exception:
                pass

    def register_listener(self, callback):
        self.listeners.append(callback)

    def unregister_listener(self, callback):
        if callback in self.listeners:
            self.listeners.remove(callback)

    def get_recent(self, count=50):
        """Return the most recent N events."""
        return list(self.events)[-count:]

    def clear(self):
        self.events.clear()


# Convenience shortcuts
def log_event(event_type, message):
    EventLogger().log(event_type, message)
