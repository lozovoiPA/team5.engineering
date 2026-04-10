from .modelvalidator import ModelValidator
from .promptrouter import PromptRouter


class ModelFactory:
    def __init__(self):
        pass

    def create_model_validator(self, model):
        mv = ModelValidator(model.connect_string)
        return mv

    def create_prompt_router(self, model):
        pr = PromptRouter(model.connect_string, model.connect_token, model.name)
        return pr