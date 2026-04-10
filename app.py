import os
import signal
import sys

import customtkinter as ctk

import services.result as results
from tkinter import messagebox

from data.entities.notification import Notification
from services.notification.notification_worker import NotificationWorker
from services.result import MeetingsRetrieved
from services.screen_text_listener import ScreenTextListener
from services.ui_worker import UiWorker
from services.model_worker import ModelWorker
from services.meeting_generation.modelfactory import ModelFactory
from dependencies import Dependencies
import threading
from data.entities.meeting import Meeting

class App:
    def __init__(self):
        self.did_init = False

        self.root = ctk.CTk()
        self.root.withdraw()

        signal.signal(signal.SIGINT, self.shutdown)

        self.dependencies = Dependencies()
        self.ui_worker = UiWorker(self.root, self.dependencies, lambda: self.shutdown(None, None))
        self.notif_worker = NotificationWorker(self.dependencies)
        self.text_listener = ScreenTextListener()

    # Called to postpone initializing most functionality! For example when we
    # only need to send notifications. And the user doesn't press it
    def init(self):
        self.did_init = True
        self.text_listener.launch(self.catch_text_from_daemon)

    def launch(self):
        if not self.did_init:
            self.init()
        self.ui_worker.show_main_window()

    def shutdown(self, signum, frame):
        print("App is shutting down (received SIGINT). Exiting...")

        try:
            self.text_listener.stop()
            if self.ui_worker.tray_icon.visible:
                self.ui_worker.tray_icon.visible = False
                self.ui_worker.tray_icon.stop()
        except Exception:
            print("Unknown exception")
        # self.root.destroy()
        # self.root.quit()
        os._exit(0)
        # sys.exit(0)

    def handle_notification(self, notif_name):
        notification = self.dependencies.notification_repo.get_notification(notif_name)
        if not isinstance(notification, Notification):
            self.shutdown(None, None)

        else:
            def click_notif(args):
                self.show_meeting_info(notification, lambda: close_notif(args))

            def close_notif(args):
                self.dependencies.notification_repo.remove_notification_by_name(notif_name)
                self.shutdown(None, None)

            def background_work():
                try:
                    self.notif_worker.send_notification(
                        notification,
                        lambda args: self.root.after(0, lambda: click_notif(args)),
                        lambda args: self.root.after(0, lambda: close_notif(args))
                    )
                except Exception:
                    self.shutdown(None, None)
            threading.Thread(target=background_work).start()

    def show_meeting_info(self, notification: Notification, on_close):
        meeting = self.dependencies.meetings_repo.get_meeting(notification.meeting_id)
        if isinstance(meeting, MeetingsRetrieved):
            meeting = meeting.meetings[0]
            self.ui_worker.show_meeting_info_window(meeting, on_close)
        else:
            on_close()

    def catch_text_from_daemon(self, text):
        self.root.after(0, lambda: self.create_meeting_from_text(text))

    def create_meeting_from_text(self, text):
        if not self.did_init:
            return
        print(text[0:300])

        def update_ui_with_result(result):
            self.ui_worker.stop_loading()
            
            if isinstance(result, results.ErrorResult):
                messagebox.showinfo("Информация", result.error_text)
                return
            
            if isinstance(result, Meeting):
                if hasattr(result, 'is_connection_error') and result.is_connection_error:
                    messagebox.showwarning("Ошибка подключения", "отсутствует доступ к LLM")
                self.ui_worker.show_meeting_window_with_prefill(result)
            else:
                self.ui_worker.show_meeting_window()

        def background_work():
            model = self.dependencies.get_model()
            factory = ModelFactory()
            toolcalls = self.dependencies.get_toolcalls()
            tools = self.dependencies.get_tools()

            mw = ModelWorker(model, factory, toolcalls, tools)
            result = mw.create_meeting_from_text(text[0:300])
            self.root.after(0, lambda: update_ui_with_result(result))

        self.ui_worker.start_loading()
        thread = threading.Thread(target=background_work)
        thread.start()
