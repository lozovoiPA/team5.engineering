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

        self.test_db_init()

    def get_model(self):
        model = Model()
        model.name = self.model_config["model_name"]
        model.connect_string = self.model_config["connect_string"]
        model.connect_token = os.getenv(self.model_config["connect_token"])
        return model

    def test_db_init(self):
        meetings = [
            Meeting("Встреча по ML", "22.04.2026", "13:35", id=1),
            Meeting("Встреча по LLM", "22.04.2026", "12:35", is_important=True, id=2),
            Meeting("Встреча 1", "22.04.2026", "11:35", id=3),
            Meeting("Встреча 2", "22.04.2026", "13:35", id=4),
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
