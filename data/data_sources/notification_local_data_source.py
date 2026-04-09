import shelve

from data.entities.notification import Notification
from services.result import ErrorResult, Result


class NotificationLocalDataSource:
    def __init__(self, shelve_path):
        self.shelve = shelve_path

    def set_notification(self, notification: Notification):
        try:
            with shelve.open(self.shelve) as db:
                db[notification.task_name] = notification
            return True
        except Exception as e:
            return ErrorResult(f"Exception trying to save notification: \n{e}")

    def get_notification(self, task_name) -> Notification | Result:
        notification = None
        try:
            with shelve.open(self.shelve) as db:
                notification = db[task_name]
            return notification
        except Exception as e:
            return ErrorResult(f"Exception trying to retrieve notification: \n{e}")

    def remove_notification(self, task_name):
        try:
            with shelve.open(self.shelve) as db:
                del db[task_name]
            return True
        except Exception as e:
            return ErrorResult(f"Exception trying to remove notification: \n{e}")
