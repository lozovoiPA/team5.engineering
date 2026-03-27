from views.MainWindow import MainWindow
from views.MeetingWindow import MeetingWindow


class UiWorker:
    def __init__(self, root, dependencies):
        self.root = root
        self.dependencies = dependencies
        self.main_window = None

    def show_main_window(self):
        self.main_window = MainWindow(self.root, on_auto_generate=self.on_auto_generate)
        self.main_window.deiconify()
        return self.main_window

    def on_auto_generate(self):
        print("Auto-generate clicked - use Alt+Shift+Z")

    def show_meeting_window_with_prefill(self, meeting):
        MeetingWindow(self.main_window, on_create=self.main_window._on_meeting_created, prefill_meeting=meeting)

    def show_meeting_window(self):
        MeetingWindow(self.main_window, on_create=self.main_window._on_meeting_created)