# logger.py
from datetime import datetime
import json

class Logger:
    _instance = None

    def __new__(cls, path="events.json"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, path="events.json"):
        self.path = path
        self.events = []

    def log(self, event_type, data):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": event_type,
            "data": data,
        }
        print(f"[LOG] {event_type} → {data}")
        self.events.append(entry)

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.events, f, indent=2)
        print(f"[LOG] Saved to {self.path}")
