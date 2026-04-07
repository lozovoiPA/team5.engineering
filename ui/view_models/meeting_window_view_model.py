from datetime import timedelta

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

    def check_collisions(self):
        delta = timedelta(hours=1)
        result = self.repository.check_collision(self.meeting, delta)

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
