import datetime
import json


class CollisionPrefs:
    def __init__(self, path):
        self.collision_window: datetime.timedelta = datetime.timedelta(minutes=30)
        self.path = path

    def get_delta_value(self):
        collision_delta = self.collision_window.total_seconds()

        mins = int(collision_delta / 60)
        hours = int(collision_delta / 3600)

        delta_flag = hours < 1
        return (mins, "mins") if delta_flag else (hours, "hours")

    def save(self):
        with open(self.path, 'w') as f:
            delta, values = self.get_delta_value()
            _dict = {"delta": delta, "values": values}
            json.dump(_dict, f)

    def open(self, _dict):
        try:
            delta = _dict["delta"]
            values = _dict["values"]
        except Exception:
            delta = 30
            values = "mins"

        if values == "hours" and 1 <= delta <= 24:
            self.collision_window = datetime.timedelta(hours=delta)
        elif values == "mins" and 20 <= delta <= 60:
            self.collision_window = datetime.timedelta(minutes=delta)
        else:
            self.collision_window = datetime.timedelta(minutes=30)


class NotificationPrefs:
    def __init__(self, path):
        self.notif_delta: datetime.timedelta = datetime.timedelta(hours=1)
        self.short_notif: bool = True
        self.path = path

    def get_delta_value(self):
        collision_delta = self.notif_delta.total_seconds()

        mins = int(collision_delta / 60)
        hours = int(collision_delta / 3600)

        delta_flag = hours < 1
        return (mins, "mins") if delta_flag else (hours, "hours")

    def save(self):
        with open(self.path, 'w') as f:
            delta, values = self.get_delta_value()
            _dict = {"delta": delta, "values": values, "short": self.short_notif}
            json.dump(_dict, f)

    def open(self, _dict):
        try:
            delta = _dict["delta"]
            values = _dict["values"]
            short = _dict["short"]
        except Exception:
            delta = 1
            values = "hours"
            short = True

        if values == "hours" and 1 <= delta <= 24:
            self.notif_delta = datetime.timedelta(hours=delta)
        elif values == "mins" and 1 <= delta <= 60:
            self.notif_delta = datetime.timedelta(minutes=delta)
        else:
            self.notif_delta = datetime.timedelta(hours=1)
        self.short_notif = short
