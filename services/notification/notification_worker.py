from win11toast import toast

from data.entities.notification import Notification
from dependencies import Dependencies
from services.result import MeetingsRetrieved


class NotificationWorker:
    def __init__(self, dependencies: Dependencies):
        self.dependencies = dependencies

    def send_notification(self, notification, on_click, on_dismissed):
        title = notification.title
        message = notification.message
        toast(title,
              message,
              on_click=on_click,
              on_dismissed=on_dismissed
        )
        # self.dependencies.notification_repo.remove_notification_by_name(notif_name)
        # self.dependencies.task_scheduler.cancel_task(notif_name)
        # self.dependencies.notification_repo.notifications_local.remove_notification(notif_name)
