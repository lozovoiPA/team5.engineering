import datetime

from data.data_sources.meeting_local_data_source import MeetingLocalDataSource
from data.entities import Model

from dotenv import load_dotenv
import os
import json
from pathlib import Path
import sys

from data.entities.meeting import Meeting
from data.meeting_database import MeetingDatabase
from data.repositories.meeting_repository import MeetingRepository
from services.result import MeetingsRetrieved


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Dependencies:
    def __init__(self):
        parent_folder = resource_path(Path(__file__).resolve().parent)
        print(parent_folder)

        dotenv_path = parent_folder / Path(".env")
        print(dotenv_path)
        load_dotenv(dotenv_path)

        config_path = parent_folder / Path("data/config")
        models = config_path / "models.json"
        with models.open('r', encoding='utf-8') as file:
            self.model_config = json.load(file)
            print(self.model_config)

        self.meetings_db = MeetingDatabase('data/localStorage.db')
        self.meetings_local_data_source = MeetingLocalDataSource(self.meetings_db)
        self.meetings_repo = MeetingRepository(self.meetings_local_data_source)

        # Создание заглушек встреч (убрать на релизе)
        res = self.meetings_local_data_source.get_meetings()
        if isinstance(res, MeetingsRetrieved) and len(res.meetings) <= 1:
            self.test_db_init()

    def get_model(self):
        model = Model()
        model.name = self.model_config["model_name"]
        model.connect_string = self.model_config["connect_string"]
        model.connect_token = os.getenv(self.model_config["connect_token"])
        return model

    def test_db_init(self):
        today = datetime.datetime.now()
        today_meet = (today + datetime.timedelta(hours=1))
        tomorrow_meet = today + datetime.timedelta(days=1)
        after_tomorrow_meet = today + datetime.timedelta(days=2)

        today_meet_date = today_meet.strftime("%d.%m.%Y")
        tomorrow_meet_date = tomorrow_meet.strftime("%d.%m.%Y")
        after_tomorrow_meet_date = after_tomorrow_meet.strftime("%d.%m.%Y")

        today_meet_time = today_meet.strftime("%H:%M")
        tomorrow_meet_time = tomorrow_meet.strftime("%H:%M")
        after_tomorrow_meet_time = after_tomorrow_meet.strftime("%H:%M")
        meetings = [
            Meeting("Встреча по ML", "22.04.2026", "13:35", id=1),
            Meeting("Встреча по LLM", "22.04.2026", "12:35", is_important=True, id=2),
            Meeting("Встреча 1", "22.04.2026", "11:35", id=3),
            Meeting("Встреча 2", "22.04.2026", "13:35", id=4),
            Meeting("Встреча сегодня", today_meet_date, today_meet_time, id=5),
            Meeting("Встреча завтра", tomorrow_meet_date, tomorrow_meet_time, id=6),
            Meeting("Встреча послезавтра", after_tomorrow_meet_date, after_tomorrow_meet_time, id=7)
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
