from win11toast import toast

from data.entities.notification import Notification
from dependencies import Dependencies


class NotificationWorker:
    def __init__(self, dependencies: Dependencies):
        self.dependencies = dependencies

    def send_notification(self, notification, on_click, on_dismissed):
        toast(notification.title,
              notification.message,
              on_click=on_click,
              on_dismissed=on_dismissed
        )
        # self.dependencies.notification_repo.remove_notification_by_name(notif_name)
        # self.dependencies.task_scheduler.cancel_task(notif_name)
        # self.dependencies.notification_repo.notifications_local.remove_notification(notif_name)
