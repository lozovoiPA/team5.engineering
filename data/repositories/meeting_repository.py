from ..data_sources.meeting_local_data_source import MeetingLocalDataSource
from ..entities.meeting import Meeting


class MeetingRepository:
    def __init__(self, meetings_local: MeetingLocalDataSource):
        self.meetings_local = meetings_local

    def save_meeting(self, meeting: Meeting):
        result = self.meetings_local.save_meeting(meeting)
        return result

    def get_meetings(self):
        result = self.meetings_local.get_meetings()
        return result

    def delete_meeting(self, meeting):
        result = self.meetings_local.delete_meeting(meeting)
        return result
