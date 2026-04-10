import services.result as results
from data.entities.meeting import Meeting
from datetime import datetime, timedelta


class ModelWorker:
    def __init__(self, model, model_factory, toolcalls, tools):
        self.model = model
        self.model_factory = model_factory
        self.toolcalls = toolcalls
        self.tools = tools

    def _get_default_datetime(self):
        now = datetime.now()
        default_time = now + timedelta(hours=1)
        minutes = default_time.minute
        rounded_minutes = (minutes // 5) * 5
        if rounded_minutes == 60:
            rounded_minutes = 0
            default_time = default_time + timedelta(hours=1)
        default_time = default_time.replace(minute=rounded_minutes, second=0, microsecond=0)
        return default_time.strftime("%d.%m.%Y"), default_time.strftime("%H:%M")

    def _create_default_meeting(self, text, is_connection_error=False):
        default_date, default_time = self._get_default_datetime()
        meeting = Meeting(
            title="Встреча",
            date=default_date,
            time=default_time,
            description=text,
            is_important=False
        )
        if is_connection_error:
            meeting.is_connection_error = True
        return meeting

    def create_meeting_from_text(self, text):
        mv = self.model_factory.create_model_validator(self.model)
        result = mv.establish_connection()
        if isinstance(result, results.ErrorResult):
            return self._create_default_meeting(text, is_connection_error=True)

        result = mv.validate_prompt(text)
        if isinstance(result, results.ErrorResult):
            return self._create_default_meeting(text, is_connection_error=True)

        pr = self.model_factory.create_prompt_router(self.model)
        prompt = pr.make_prompt(text, toolcalls=self.toolcalls)
        result = pr.execute_prompt(prompt)

        if isinstance(result, results.ErrorResult):
            if result.error_text == "CONNECTION_ERROR":
                return self._create_default_meeting(text, is_connection_error=True)
            return result

        meeting = pr.execute_toolcall(result, text)
        return meeting
