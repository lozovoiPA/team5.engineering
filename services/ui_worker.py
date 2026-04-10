import os

from ui.views import MainWindow
from ui.views import MeetingWindow

import customtkinter as ctk

from ui.views.loader import CircularLoader

from pystray import Icon as TrayIcon, MenuItem as item
from PIL import Image, ImageDraw

from ui.views.meeting_info_window import MeetingInfoWindow
from ui.views.settings_window import SettingsWindow


def create_image():
    image = Image.new('RGB', (64, 64), color='blue')
    return image


def center_window(top: ctk.CTkToplevel, window_width=None, window_height=None):
    window_width = top.winfo_width() if window_width is None else window_width
    window_height = top.winfo_height() if window_height is None else window_height

    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    top.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


class UiWorker:
    def __init__(self, root, dependencies, on_shutdown):
        self.root = root
        self.dependencies = dependencies
        self.main_window = None
        self.loading_toplevel = None
        self.on_shutdown = on_shutdown

        self.tray_icon_image = create_image()
        self.tray_menu = (item('Show', self._show_window, default=True), item('Quit', self._quit_window))
        self.tray_icon = TrayIcon("name", self.tray_icon_image, "Smartmeet", self.tray_menu)

    def minimize(self):
        self.main_window.withdraw()
        self.tray_menu = (item('Show', self._show_window, default=True), item('Quit', self._quit_window))
        self.tray_icon = TrayIcon("name", self.tray_icon_image, "Smartmeet", self.tray_menu)
        self.tray_icon.run()

    def show_main_window(self):
        if self.main_window is None:
            self.main_window = MainWindow(
                self.root,
                self.dependencies.meetings_repo,
                on_close=self.minimize,
                on_settings=self.show_settings_window
            )
        else:
            self.main_window.deiconify()
        return self.main_window

    def _quit_window(self, icon, item):
        self.tray_icon.visible = False
        self.tray_icon.stop()
        self.close_main_window()
        self.root.after(30, self.on_shutdown(None, None))

    def _show_window(self, icon, item):
        self.tray_icon.stop()
        self.show_main_window()

    def close_main_window(self):
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

    def show_settings_window(self):
        swnd = SettingsWindow(self.root, self.dependencies.collision_prefs, self.dependencies.notification_prefs)
        swnd.attributes('-topmost', True)
        swnd.attributes('-topmost', False)
        swnd.transient(self.main_window)
        swnd.grab_set()
        swnd.focus_set()

    def show_meeting_info_window(self, meeting, on_close):
        center_window(MeetingInfoWindow(self.root, meeting, on_close), 450, 400)
