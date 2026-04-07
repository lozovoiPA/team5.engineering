from tkinter import messagebox

from data.repositories.meeting_repository import MeetingRepository
from services.result import ErrorResult, MeetingsRetrieved, MeetingsDeleted, MeetingsUpdated
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

    def _filter_close(self, days_diff):
        return 0 <= days_diff < 3

    def _filter_today(self, days_diff):
        return days_diff == 0

    def _filter_week(self, days_diff):
        return 0 <= days_diff <= 7

    def _apply_filter(self, meeting, current_date=None, days_diff=None, filter_type=None):
        if days_diff is None:
            if current_date is None:
                current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            meeting_date = datetime.strptime(meeting.date, "%d.%m.%Y")
            meeting_date = meeting_date.replace(hour=0, minute=0, second=0, microsecond=0)
            days_diff = (meeting_date - current_date).days
        if filter_type is None:
            filter_type = self.filter
        return (
                (filter_type == "Ближайшие" and self._filter_close(days_diff)) or
                (filter_type == "На день" and self._filter_today(days_diff)) or
                (filter_type == "На неделю" and self._filter_week(days_diff)) or
                (filter_type == "Важные" and meeting.is_important)
        )

    def _sort_and_display(self, meetings):
        try:
            meetings.sort(key=lambda m: (
                datetime.strptime(m.date, "%d.%m.%Y") if m.date else datetime.max,
                m.time if m.time else "23:59"
            ))
            self.display_meetings = meetings
        except Exception as e:
            print(f"{e}")

    def add_meeting(self, meeting):
        if meeting not in self.meetings:
            self.meetings.append(meeting)
        if self._apply_filter(meeting):
            filtered = self.display_meetings + [meeting]
            self._sort_and_display(filtered)

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

                    if self._apply_filter(meeting, days_diff=days_diff):
                        filtered.append(meeting)
                except Exception as e:
                    print(f"Ошибка парсинга даты {meeting.date}: {e}")
        self._sort_and_display(filtered)

    def delete_meeting(self, meeting):
        result = self.repository.delete_meeting(meeting)
        if isinstance(result, ErrorResult):
            print(result.error_text)
            return False
        elif isinstance(result, MeetingsDeleted):
            self.meetings.remove(meeting)
            if meeting in self.display_meetings:
                self.display_meetings.remove(meeting)
            return True
        else:
            print("Unknown error in MainWindowViewModel.delete_meeting()")
            return False

    def toggle_importance(self, meeting):
        meeting.is_important = not meeting.is_important
        result = self.repository.save_meeting(meeting)
        if isinstance(result, ErrorResult):
            print(result.error_text)
            return False
        elif isinstance(result, MeetingsUpdated):
            return True
        else:
            print("Unknown error in MainWindowViewModel.toggle_importance()")
            return False
