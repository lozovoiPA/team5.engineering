from entities.model import Model
from entities.toolcall import ToolCall

from dotenv import load_dotenv
import os
import json
from pathlib import Path

# Define the folder and file name


class Dependencies:
    def __init__(self):
        load_dotenv()
        
        folder = Path(__file__).resolve().parent
        config_path = folder / Path("data/config")
        models = config_path / "models.json"
        with models.open('r', encoding='utf-8') as file:
            self.model_config = json.load(file)

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