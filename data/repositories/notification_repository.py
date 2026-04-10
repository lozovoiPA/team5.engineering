import traceback
from datetime import datetime, timedelta

from data.data_sources.notification_local_data_source import NotificationLocalDataSource
from data.entities.meeting import Meeting
from data.entities.notification import Notification
from prefs import NotificationPrefs
from services.notification.task_scheduler import TaskScheduler
from services.result import ErrorResult, TaskSchedulerSuccess


class NotificationRepository:
    def __init__(self, notifications_local: NotificationLocalDataSource, scheduler: TaskScheduler,
                 notification_prefs: NotificationPrefs):
        self.notifications_local = notifications_local

        self.scheduler = scheduler
        self.notification_prefs = notification_prefs

    def meeting_to_notif(self, meeting: Meeting):
        notification = Notification()
        notification.task_name = f"m_{meeting.id}"
        notification.title = f"{meeting.title}"
        notification.message = f"Начнется в {meeting.time} {meeting.date}" if self.notification_prefs.short_notif else f"Встреча скоро начнется!\n{meeting.description}. Приходите к {meeting.time} {meeting.date}"
        notification.meeting_id = meeting.id
        notification.timestamp = datetime.strptime(meeting.date + ' ' + meeting.time,
                                                   '%d.%m.%Y %H:%M') - self.notification_prefs.notif_delta
        return notification

    def ensure_time(self, meeting: Meeting):
        meeting_timestamp = datetime.strptime(meeting.date + ' ' + meeting.time,
                                              '%d.%m.%Y %H:%M')
        notification_time = meeting_timestamp - self.notification_prefs.notif_delta

        now_time = datetime.now().replace(second=0, microsecond=0)
        if now_time > notification_time:
            notification_time = now_time + timedelta(minutes=1)
        return notification_time

    def get_notification(self, notif_name):
        return self.notifications_local.get_notification(notif_name)

    def remove_notification_by_name(self, notif_name):
        try:
            self.scheduler.cancel_task(f"{notif_name}")
        except Exception as e:
            error_text = f'''
                Error in NotificationWorker.remove_notification():
                {e}
            '''
            return ErrorResult(error_text)

        result = self.notifications_local.remove_notification(f"{notif_name}")
        if not isinstance(result, ErrorResult):
            result = TaskSchedulerSuccess()
        return result

    def remove_notification(self, meeting: Meeting):
        return self.remove_notification_by_name(f"m_{meeting.id}")

    def update_notification(self, meeting: Meeting):
        try:
            notification = self.notifications_local.get_notification(f"m_{meeting.id}")
        except Exception as e:
            error_text = f'''
                            Error in NotificationWorker.update_notification():
                            {e}
                        '''
            return ErrorResult(error_text)

        try:
            notification_time = self.ensure_time(meeting)

            flag = True
            if notification.timestamp != notification_time:
                flag = self.scheduler.postpone_task(f"m_{meeting.id}", notification_time)
            notification = self.meeting_to_notif(meeting)
            self.notifications_local.set_notification(notification)
            return TaskSchedulerSuccess() if flag else ErrorResult('Meeting notification was not updated')
        except Exception as e:
            error_text = f'''
                            Error in NotificationWorker.update_notification():
                            {e}
                        '''
            return ErrorResult(error_text)

    def plan_meeting_notification(self, meeting: Meeting):
        notification = self.meeting_to_notif(meeting)
        notification.timestamp = self.ensure_time(meeting)

        script_args = f"--send-notif \"{notification.task_name}\""

        try:
            self.scheduler.create_notification_task(
                notification.task_name,
                notification.timestamp,
                script_args
            )
            self.notifications_local.set_notification(notification)
            return TaskSchedulerSuccess()
        except Exception as e:
            error_text = f'''
                Error in NotificationWorker.plan_meeting_notification():
                {e}
            '''
            print(error_text, traceback.format_exc())
            return ErrorResult(error_text)
