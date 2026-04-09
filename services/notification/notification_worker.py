from win11toast import toast

from data.entities.notification import Notification
from dependencies import Dependencies


class NotificationWorker:
    def __init__(self, dependencies: Dependencies):
        self.dependencies = dependencies

    def send_notification(self, notif_name, on_click, on_dismissed):
        notification = self.dependencies.notification_repo.get_notification(notif_name)
        if isinstance(notification, Notification):
            toast(notification.title,
                  notification.message,
                  on_click=on_click,
                  on_dismissed=on_dismissed
                  )
        self.dependencies.notification_repo.remove_notification_by_name(notif_name)
        # self.dependencies.task_scheduler.cancel_task(notif_name)
        # self.dependencies.notification_repo.notifications_local.remove_notification(notif_name)
