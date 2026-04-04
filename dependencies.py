from data.entities import Model

from dotenv import load_dotenv
import os
import json
from pathlib import Path
import sys


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

    def get_model(self):
        model = Model()
        model.name = self.model_config["model_name"]
        model.connect_string = self.model_config["connect_string"]
        model.connect_token = os.getenv(self.model_config["connect_token"])
        return model

    def get_toolcalls(self):
        tools = []
        return tools

    def get_tools(self):
        TOOL_MAPPING = {}
        return TOOL_MAPPING
