import datetime
from datetime import timedelta

from services.result import MeetingsCreated, MeetingsUpdated, MeetingsDeleted
from .notification_repository import NotificationRepository
from ..data_sources.meeting_local_data_source import MeetingLocalDataSource
from ..entities.meeting import Meeting


class MeetingRepository:
    def __init__(self, meetings_local: MeetingLocalDataSource, notif_repo: NotificationRepository):
        self.meetings_local = meetings_local
        self.notif_repo = notif_repo

    def save_meeting(self, meeting: Meeting):
        if meeting.id is not None:
            result = self.meetings_local.update_meeting(meeting)
            if isinstance(result, MeetingsUpdated):
                notif_result = self.notif_repo.update_notification(meeting)
        else:
            result = self.meetings_local.save_meeting(meeting)
            if isinstance(result, MeetingsCreated):
                notif_result = self.notif_repo.plan_meeting_notification(meeting)
        return result

    def get_meetings(self):
        result = self.meetings_local.get_meetings()
        return result

    def get_meeting(self, meeting_id):
        result = self.meetings_local.get_meeting(meeting_id)
        return result

    def delete_meeting(self, meeting):
        result = self.meetings_local.delete_meeting(meeting)
        if isinstance(result, MeetingsDeleted):
            notif_result = self.notif_repo.remove_notification(meeting)
        return result

    def check_collision(self, meeting: Meeting, delta: timedelta):
        timestamp = datetime.datetime.strptime(meeting.date + ' ' + meeting.time, '%d.%m.%Y %H:%M')
        result = self.meetings_local.check_collisions(meeting, timestamp, delta)

        return result
