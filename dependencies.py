from entities.model import Model
from entities.toolcall import ToolCall


class Dependencies:
    def __init__(self):
        pass

    def get_model(self):
        model = Model()
        model.name = "gpt-4o-mini"
        model.connect_string = "https://api.aitunnel.ru/v1"
        model.connect_token = "sk-aitunnel-"
        return model

    def get_toolcalls(self):
        tools = []
        return tools

    def get_tools(self):
        TOOL_MAPPING = {}
        return TOOL_MAPPING