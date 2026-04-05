from sqlalchemy import select
from datetime import datetime

from sqlalchemy.orm import Session

from services.result import MeetingsRetrieved, ErrorResult, MeetingsCreated, MeetingsDeleted
from ..entities.meeting import Meeting
from ..meeting_database import MeetingDb, MeetingDatabase


def meeting_to_db(meeting: Meeting):
    meeting_db = MeetingDb()
    meeting_db.name = meeting.title
    meeting_db.priority = meeting.is_important
    meeting_db.timestamp = datetime.strptime(meeting.date + ' ' + meeting.time,
                                             '%d.%m.%Y %H:%M')
    meeting_db.description = meeting.description
    meeting_db.id = meeting.id
    return meeting_db


def meeting_from_db(meeting_db: MeetingDb):
    meeting = Meeting()
    meeting.title = meeting_db.name
    meeting.is_important = meeting_db.priority
    meeting.date = meeting_db.timestamp.date().strftime("%d.%m.%Y")
    meeting.time = meeting_db.timestamp.time().strftime("%H:%M")
    meeting.description = meeting_db.description
    meeting.id = meeting_db.id
    return meeting


class MeetingLocalDataSource:
    def __init__(self, db: MeetingDatabase):
        self.db = db

    def save_meeting(self, meeting: Meeting):
        meeting_db = meeting_to_db(meeting)

        def query(session):
            session.add(meeting_db)

        try:
            self.db.execute_query(query)
            print(f"Meeting created with id {meeting_db.id}")
            return MeetingsCreated()
        except Exception as e:
            return ErrorResult(f'''
            Exception in MeetingLocalDataSource.save_meeting();
            {e}
            ''')

    def get_meetings(self):
        def query(session):
            _meetings = [meeting_from_db(meeting) for meeting in session.scalars(select(MeetingDb)).all()]
            return _meetings

        try:
            meetings = self.db.execute_query(query)
            return MeetingsRetrieved(meetings)
        except Exception as e:
            return ErrorResult(f'''
            Exception in MeetingLocalDataSource.get_meetings();
            {e}
            ''')

    def delete_meeting(self, meeting):
        def query(session: Session):
            meeting_db = session.get(MeetingDb, meeting.id)
            if meeting_db is None:
                return ErrorResult("Meeting not found")
            session.delete(meeting_db)
            return MeetingsDeleted()

        try:
            result = self.db.execute_query(query)
            return result
        except Exception as e:
            return ErrorResult(f'''
                        Exception in MeetingLocalDataSource.delete_meeting();
                        {e}
                        ''')
