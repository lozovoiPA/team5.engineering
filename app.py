import os
import signal
import sys

import customtkinter as ctk

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
        self.ui_worker = UiWorker(self.root, self.dependencies, self.shutdown)
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

        self.text_listener.stop()
        self.root.destroy()
        os._exit(0)
        # sys.exit(0)

    def handle_notification(self, notif_name):
        notification = self.dependencies.notification_repo.get_notification(notif_name)
        if not isinstance(notification, Notification):
            self.shutdown(None, None)

        else:
            def background_work():
                self.notif_worker.send_notification(
                    notification,
                    lambda args: self.root.after(0, lambda: self.show_meeting_info(notification)),
                    lambda args: self.root.after(0, lambda: self.shutdown(None, None))
                )
            threading.Thread(target=background_work).start()

    def show_meeting_info(self, notification: Notification):
        meeting = self.dependencies.meetings_repo.get_meeting(notification.meeting_id)
        if isinstance(meeting, MeetingsRetrieved):
            meeting = meeting.meetings[0]
            self.ui_worker.show_meeting_info_window(meeting, lambda: self.shutdown(None, None))
        else:
            self.shutdown(None, None)

    def catch_text_from_daemon(self, text):
        self.root.after(0, lambda: self.create_meeting_from_text(text))

    def create_meeting_from_text(self, text):
        if not self.did_init:
            return
        print(text[0:300])

        def update_ui_with_result(result):
            self.ui_worker.stop_loading()
            if isinstance(result, Meeting):
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
