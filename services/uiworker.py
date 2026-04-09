from ui.views import MainWindow
from ui.views import MeetingWindow

import customtkinter as ctk

from ui.views.loader import CircularLoader


def center_window(top: ctk.CTkToplevel, window_width=None, window_height=None):
    window_width = top.winfo_width() if window_width is None else window_width
    window_height = top.winfo_height() if window_height is None else window_height

    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    top.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

class UiWorker:
    def __init__(self, root, dependencies):
        self.root = root
        self.dependencies = dependencies
        self.main_window = None
        self.loading_toplevel = None

    def show_main_window(self):
        self.main_window = MainWindow(self.root, self.dependencies.meetings_repo, on_close=self._close_main_window)
        # self.main_window.deiconify()
        return self.main_window

    def _close_main_window(self):
        self.main_window.destroy()
        self.main_window = None

    def start_loading(self):
        if self.loading_toplevel is not None:
            self.loading_toplevel.destroy()
        self.loading_toplevel = ctk.CTkToplevel()
        center_window(self.loading_toplevel, 300, 90)
        self.loading_toplevel.resizable(False, False)

        # self.loading_toplevel.protocol("WM_DELETE_WINDOW", lambda: print("Loading window cannot be closed"))
        self.loading_toplevel.overrideredirect(True)

        wait_tip = ctk.CTkLabel(self.loading_toplevel, text=f"Подождите...ваш запрос обрабатывается...", text_color="#555555", font=ctk.CTkFont(size=14))
        wait_tip.pack(expand=True)

        loader = CircularLoader(self.loading_toplevel, size=50, color="#1e90ff", bgcolor="#eeeeee")
        loader.pack(expand=True)
        self.loading_toplevel.config(cursor="watch")

    def stop_loading(self):
        if self.loading_toplevel is None:
            return
        self.loading_toplevel.destroy()
        self.loading_toplevel = None

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
