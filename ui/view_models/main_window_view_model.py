from tkinter import messagebox

from data.repositories.meeting_repository import MeetingRepository
from services.result import ErrorResult, MeetingsRetrieved, MeetingsDeleted
from datetime import datetime


class MainWindowViewModel:
    def __init__(self, repository: MeetingRepository):
        self.repository = repository

        self.meetings = []
        self.display_meetings = []

        self.error_display = False
        self.error_text = ""
        self.error_log = ""

        self.filter = ""
        self.loading = False
        self.loader_angle = 0

    def get_meetings(self):
        result = self.repository.get_meetings()

        if isinstance(result, ErrorResult):
            self.error_display = True
            self.error_text = "Ошибка: не удалось найти встречи"
            self.error_log = result.error_text

            print(self.error_log)

        elif isinstance(result, MeetingsRetrieved):
            self.meetings = result.meetings
            self.display_meetings = self.meetings
        else:
            self.error_display = True
            self.error_text = "Неизвестная ошибка"
            self.error_log = ""

            print(self.error_log)

    def filter_meetings(self, filter_type):
        if self.filter == filter_type:
            return
        self.filter = filter_type
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        filtered = []
        if filter_type == "Все":
            filtered = self.meetings
        else:
            for meeting in self.meetings:
                try:
                    meeting_date = datetime.strptime(meeting.date, "%d.%m.%Y")
                    meeting_date = meeting_date.replace(hour=0, minute=0, second=0, microsecond=0)
                    days_diff = (meeting_date - current_date).days

                    if filter_type == "Ближайшие":
                        if 0 <= days_diff < 3:
                            filtered.append(meeting)
                    elif filter_type == "На день":
                        if days_diff == 0:
                            filtered.append(meeting)
                    elif filter_type == "На неделю":
                        if 0 <= days_diff <= 7:
                            filtered.append(meeting)
                    elif filter_type == "Важные":
                        if meeting.is_important:
                            filtered.append(meeting)
                except Exception as e:
                    print(f"Ошибка парсинга даты {meeting.date}: {e}")
                    filtered.append(meeting)

        try:
            filtered.sort(key=lambda m: (
                datetime.strptime(m.date, "%d.%m.%Y") if m.date else datetime.max,
                m.time if m.time else "23:59"
            ))
            self.display_meetings = filtered
        except Exception as e:
            print(f"{e}")

    def delete_meeting(self, meeting):
        if messagebox.askyesno("Удаление", f"Удалить встречу «{meeting.title}»?"):
            result = self.repository.delete_meeting(meeting)
            if isinstance(result, ErrorResult):
                print(result.error_text)
            elif isinstance(result, MeetingsDeleted):
                self.meetings.remove(meeting)
                if meeting in self.display_meetings:
                    self.display_meetings.remove(meeting)
            else:
                print("Unknown error in MainWindowViewModel.delete_meeting()")

    def toggle_importance(self, meeting):
        meeting.is_important = not meeting.is_important
