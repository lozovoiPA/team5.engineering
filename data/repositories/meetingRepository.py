from ..dataSources.meetingLocalDataSource import MeetingsLocalDataSource
from ..entities.meeting import Meeting


class MeetingRepository:
    def __init__(self, meetings_local: MeetingsLocalDataSource):
        self.meetings_local = meetings_local

    def save_meeting(self, meeting: Meeting):
        self.meetings_local.save_meeting(meeting)
