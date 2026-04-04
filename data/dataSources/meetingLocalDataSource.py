from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker

from ..entities.meeting import Meeting
from ..meetingDatabase import MeetingDb


def meeting_to_db(meeting):
    meeting_db = MeetingDb()
    meeting_db.name = meeting.title
    meeting_db.priority = meeting.is_important
    meeting_db.date = meeting.date
    meeting_db.time = meeting.time
    meeting_db.description = meeting.description
    return meeting_db


class MeetingsLocalDataSource:
    def __init__(self, engine: Engine):
        self.engine = engine

    def save_meeting(self, meeting: Meeting):
        meeting_db = meeting_to_db(meeting)

        with sessionmaker(bind=self.engine).begin() as session:
            session.add(meeting_db)
