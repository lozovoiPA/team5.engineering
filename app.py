import signal
import sys

import customtkinter as ctk
from services.screen_text_listener import ScreenTextListener
from services.uiworker import UiWorker
from services.modelworker import ModelWorker
from services.meeting_generation.modelfactory import ModelFactory
from dependencies import Dependencies
import threading
from data.entities.meeting import Meeting


class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.withdraw()

        signal.signal(signal.SIGINT, self.shutdown)

        self.dependencies = Dependencies()
        self.uiworker = UiWorker(self.root, self.dependencies)
        self.text_listener = ScreenTextListener()

        self.text_listener.launch(self.catch_text_from_daemon)

    def launch(self):
        self.uiworker.show_main_window()

    def shutdown(self, signum, frame):
        print("App is shutting down (received SIGINT). Exiting...")

        self.text_listener.stop()
        self.root.destroy()
        sys.exit(0)

    def catch_text_from_daemon(self, text):
        self.root.after(0, lambda: self.create_meeting_from_text(text))

    def create_meeting_from_text(self, text):
        print(text[0:300])

        def background_work():
            model = self.dependencies.get_model()
            factory = ModelFactory()
            toolcalls = self.dependencies.get_toolcalls()
            tools = self.dependencies.get_tools()

            mw = ModelWorker(model, factory, toolcalls, tools)
            result = mw.create_meeting_from_text(text[0:300])
            self.root.after(0, lambda: self.update_ui_with_result(result))

        self.uiworker.start_loading()
        thread = threading.Thread(target=background_work)
        thread.start()

    def update_ui_with_result(self, result):
        self.uiworker.stop_loading()

        if isinstance(result, Meeting):
            self.uiworker.show_meeting_window_with_prefill(result)
        else:
            self.uiworker.show_meeting_window()
