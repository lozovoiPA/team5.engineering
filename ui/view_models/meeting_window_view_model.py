from datetime import timedelta, datetime

from data.entities.meeting import Meeting
from data.repositories.meeting_repository import MeetingRepository
from services.result import MeetingsRetrieved, ErrorResult, MeetingsCreated, MeetingsUpdated


class MeetingWindowViewModel:
    def __init__(self, repository: MeetingRepository, meeting: Meeting = None):
        self.repository: MeetingRepository = repository
        self.meeting: Meeting = meeting

    def save_meeting(self):
        result = self.repository.save_meeting(self.meeting)
        if isinstance(result, ErrorResult):
            print(f"Error in saving meeting:\n{result.error_text}")
            return False
        elif isinstance(result, MeetingsCreated | MeetingsUpdated):
            return True
        else:
            print(f"Unknown error in saving meeting.")
            return False
        pass

    def is_valid_date(self, day, month, year):
        try:
            datetime(int(year), int(month), int(day))
            return True
        except Exception as e:
            return False

    def is_valid_time(self, time_str):
        if not time_str or len(time_str) != 5:
            return False
        if time_str[2] != ':':
            return False
        try:
            hours = int(time_str[:2])
            minutes = int(time_str[3:])
            return 0 <= hours <= 23 and 0 <= minutes <= 59
        except Exception as e:
            return False

    def check_collisions(self):
        result = self.repository.check_collision(self.meeting)

        print("MeetingWindowViewModel.check_collision() started...")
        if isinstance(result, MeetingsRetrieved):
            if len(result.meetings) == 0:
                print("No collisions found.")
                return
            print("Collision with:")
            for m in result.meetings:
                print(f"{m.title} ({m.date} {m.time})")
            return result.meetings
        elif isinstance(result, ErrorResult):
            print(f"Error:\n{result.error_text}")
        else:
            print("Unknown error.")
