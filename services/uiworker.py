from ui.views import MainWindow
from ui.views import MeetingWindow


class UiWorker:
    def __init__(self, root, dependencies):
        self.root = root
        self.dependencies = dependencies
        self.main_window = None

    def show_main_window(self):
        self.main_window = MainWindow(self.root, self.dependencies.meetings_repo, on_close=self._close_main_window)
        # self.main_window.deiconify()
        return self.main_window

    def _close_main_window(self):
        self.main_window.destroy()
        self.main_window = None

    def show_meeting_window_with_prefill(self, meeting):
        if self.main_window is not None:
            parent = self.main_window
            on_save = self.main_window.on_meeting_saved

        else:
            parent = self.root
            on_save = None
        MeetingWindow(parent, prefill_meeting=meeting, repository=self.dependencies.meetings_repo, on_save=on_save)

    def show_meeting_window(self):
        if self.main_window is not None:
            parent = self.main_window
            on_save = self.main_window.on_meeting_saved
        else:
            parent = self.root
            on_save = None
        MeetingWindow(parent, repository=self.dependencies.meetings_repo, on_save=on_save)
