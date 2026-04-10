import datetime

from data.data_sources.meeting_local_data_source import MeetingLocalDataSource
from data.data_sources.notification_local_data_source import NotificationLocalDataSource
from data.entities import Model

from dotenv import load_dotenv
import os
import json
from pathlib import Path
import sys

from data.entities.meeting import Meeting
from data.meeting_database import MeetingDatabase
from data.repositories.meeting_repository import MeetingRepository
from data.repositories.notification_repository import NotificationRepository
from prefs import CollisionPrefs, NotificationPrefs
from services.notification.task_scheduler import TaskScheduler
from services.result import MeetingsRetrieved


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def open_json(path):
    data = None
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        return data
    except Exception:
        return data


class Dependencies:
    def __init__(self):
        self.parent_folder = str(resource_path(Path(__file__).resolve().parent))
        print(self.parent_folder)

        dotenv_path = self.parent_folder / Path(".env")
        print(dotenv_path)
        load_dotenv(dotenv_path)

        config_path = self.parent_folder / Path("data/config")
        models = config_path / "models.json"
        with models.open('r', encoding='utf-8') as file:
            self.model_config = json.load(file)
            print(self.model_config)

        self.meetings_db = MeetingDatabase(self.parent_folder / Path('data/localStorage.db'))
        self.meetings_local_data_source = MeetingLocalDataSource(self.meetings_db)
        self.notifications_local_data_source = NotificationLocalDataSource(
            self.parent_folder / Path("data/notification_shelf.db"))

        if not getattr(sys, 'frozen', False):
            exe_path = f"\"{os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')}\""
            script_path = f"{self.parent_folder / Path('main.py')}"
            script_folder = f"{os.path.dirname(script_path)}"
            script_path = f"\"{script_path}\""
        else:
            exe_path = sys.executable
            script_path = None
            script_folder = self.parent_folder

        self.task_scheduler = TaskScheduler(exe_path, script_folder, script_path)

        col_path = config_path / Path('collision_prefs.json')
        notif_path = config_path / Path('notif_prefs.json')

        self.collision_prefs = CollisionPrefs(col_path)
        self.notification_prefs = NotificationPrefs(notif_path)

        col_prefs_dict = open_json(col_path)
        notif_prefs_dict = open_json(notif_path)

        if col_prefs_dict is not None:
            self.collision_prefs.open(col_prefs_dict)

        if notif_prefs_dict is not None:
            self.notification_prefs.open(notif_prefs_dict)

        self.notification_repo: NotificationRepository = NotificationRepository(
            self.notifications_local_data_source,
            self.task_scheduler,
            self.notification_prefs
        )
        self.meetings_repo = MeetingRepository(
            self.meetings_local_data_source,
            self.notification_repo,
            self.collision_prefs
        )

        if not getattr(sys, 'frozen', False):
            res = self.meetings_local_data_source.get_meetings()
            if isinstance(res, MeetingsRetrieved):
                print(f"Найдено: {len(res.meetings)} встреч")
                if len(res.meetings) <= 1:
                    self.test_db_init()

    def get_model(self):
        model = Model()
        model.name = self.model_config["model_name"]
        model.connect_string = self.model_config["connect_string"]
        model.connect_token = os.getenv(self.model_config["connect_token"])
        return model

    def test_db_init(self):
        print("Создаю заглушки встреч...")
        today = datetime.datetime.now()
        today_meet = (today + datetime.timedelta(minutes=2))
        tomorrow_meet = today + datetime.timedelta(days=1)
        after_tomorrow_meet = today + datetime.timedelta(days=2)

        today_meet_date = today_meet.strftime("%d.%m.%Y")
        tomorrow_meet_date = tomorrow_meet.strftime("%d.%m.%Y")
        after_tomorrow_meet_date = after_tomorrow_meet.strftime("%d.%m.%Y")

        today_meet_time = today_meet.strftime("%H:%M")
        tomorrow_meet_time = tomorrow_meet.strftime("%H:%M")
        after_tomorrow_meet_time = after_tomorrow_meet.strftime("%H:%M")
        meetings = [
            Meeting("Встреча по ML", "22.04.2026", "13:35"),
            Meeting("Встреча по LLM", "22.04.2026", "12:35", is_important=True),
            Meeting("Встреча 1", "22.04.2026", "11:35"),
            Meeting("Встреча 2", "22.04.2026", "13:35"),
            Meeting("Встреча сегодня", today_meet_date, today_meet_time),
            Meeting("Встреча завтра", tomorrow_meet_date, tomorrow_meet_time),
            Meeting("Встреча послезавтра", after_tomorrow_meet_date, after_tomorrow_meet_time)
        ]
        for m in meetings:
            self.meetings_repo.save_meeting(m)

    def get_toolcalls(self):
        tools = []
        return tools

    def get_tools(self):
        TOOL_MAPPING = {}
        return TOOL_MAPPING

    def get_meeting_local_data_source(self):
        return self.meetings_local_data_source
