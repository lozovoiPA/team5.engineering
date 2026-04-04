from data.repositories.meeting_repository import MeetingRepository
from services.result import ErrorResult, MeetingsRetrieved


class MainWindowViewModel:
    def __init__(self, repository: MeetingRepository):
        self.repository = repository

        self.meetings = []

        self.error_display = False
        self.error_text = ""
        self.error_log = ""

    def get_meetings(self):
        result = self.repository.get_meetings()
        if isinstance(result, ErrorResult):
            self.error_display = True
            self.error_text = "Ошибка: не удалось найти встречи"
            self.error_log = result.error_text

            print(self.error_log)

        elif isinstance(result, MeetingsRetrieved):
            self.meetings = result.meetings
        else:
            self.error_display = True
            self.error_text = "Неизвестная ошибка"
            self.error_log = ""

            print(self.error_log)
