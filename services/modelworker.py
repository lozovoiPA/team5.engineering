import services.result as results


class ModelWorker:
    def __init__(self, model, model_factory, toolcalls, tools):
        self.model = model
        self.model_factory = model_factory
        self.toolcalls = toolcalls
        self.tools = tools

    def create_meeting_from_text(self, text):
        mv = self.model_factory.create_model_validator(self.model)
        result = mv.establish_connection()
        if isinstance(result, results.ErrorResult):
            return result

        result = mv.validate_prompt(text)
        if isinstance(result, results.ErrorResult):
            return result

        pr = self.model_factory.create_prompt_router(self.model)
        prompt = pr.make_prompt(text, toolcalls=self.toolcalls)
        result = pr.execute_prompt(prompt)

        if isinstance(result, results.ErrorResult):
            return result

        meeting = pr.execute_toolcall(result, text)
        return meeting