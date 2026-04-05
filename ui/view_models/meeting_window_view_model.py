from datetime import timedelta

from data.repositories.meeting_repository import MeetingRepository
from services.result import MeetingsRetrieved


class MeetingWindowViewModel:
    def __init__(self, repository: MeetingRepository):
        self.repository = repository

    def check_collisions(self, meeting):
        delta = timedelta(hours=1)
        result = self.repository.check_collision(meeting, delta)

        print("view model collision checking")
        if isinstance(result, MeetingsRetrieved):
            if len(result.meetings) == 0:
                print("No collisione my amigo !")
                return
            print("Collision with:")
            for m in result.meetings:
                print(f"{m.title} ({m.date} {m.time})")
        else:
            print("eror in collision chewcking!! plweease chweck!!")
