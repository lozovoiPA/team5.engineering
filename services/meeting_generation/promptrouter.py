import json
from openai import OpenAI
from datetime import date, timedelta
from data.entities.meeting import Meeting
from data.entities.prompt import Prompt
import services.result as results


class PromptRouter:
    def __init__(self, connect_string, connect_token, model_name):
        self.connect_string = connect_string
        self.connect_token = connect_token
        self.model_name = model_name

    def make_prompt(self, text, history=[], toolcalls=[]):
        prompt = Prompt()
        prompt.text = text
        prompt.history = history
        prompt.toolcalls = toolcalls
        return prompt

    def execute_prompt(self, prompt):
        today = date.today()
        today_str = today.isoformat()
        tomorrow = (today + timedelta(days=1)).isoformat()
        day_after = (today + timedelta(days=2)).isoformat()

        days_ahead = (3 - today.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        thursday = (today + timedelta(days=days_ahead)).isoformat()

        system = f"""Сегодня {today_str}.
Завтра = {tomorrow}
Послезавтра = {day_after}
Ближайший четверг = {thursday}

Верни только JSON.

Если в тексте НЕТ информации о встрече, верни:
{{"error": "no_meeting_info"}}

Если информация о встрече есть, верни:
{{
    "meeting_date": "YYYY-MM-DD",
    "meeting_time": "HH:MM",
    "topic": "название",
    "summary": "описание"
}}

Правила времени:
- "пол 1", "пол первого" -> "12:30"
- "пол 5" -> "16:30"
- "в 2 часа", "в два часа" -> "14:00"
- "через X часов" -> текущее время + X часов

Без объяснений, только JSON."""

        user_prompt = f"Текст: {prompt.text}"

        try:
            client = OpenAI(
                api_key=self.connect_token,
                base_url=self.connect_string
            )

            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.0,
                max_tokens=200,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            data = json.loads(content)

            if data.get("error") == "no_meeting_info":
                return results.ErrorResult("Нет информации о встрече по версии LLM")

            return data

        except Exception as e:
            error_msg = str(e)
            print(f"ExecutePrompt error: {error_msg}")

            if "Connection error" in error_msg or "connect" in error_msg.lower():
                return results.ErrorResult("CONNECTION_ERROR")

            return results.ErrorResult(f"Ошибка при обработке: {error_msg}")

    def execute_toolcall(self, toolcall, text):
        if isinstance(toolcall, results.ErrorResult):
            return toolcall

        try:
            meeting_date = toolcall.get("meeting_date", "")
            try:
                if meeting_date:
                    d = date.fromisoformat(meeting_date)
                    date_str = d.strftime("%d.%m.%Y")
                else:
                    tomorrow = date.today() + timedelta(days=1)
                    date_str = tomorrow.strftime("%d.%m.%Y")
            except Exception:
                tomorrow = date.today() + timedelta(days=1)
                date_str = tomorrow.strftime("%d.%m.%Y")

            meeting_time = toolcall.get("meeting_time", "14:00")
            if meeting_time == "не указано":
                return results.ErrorResult("CONNECTION_ERROR")

            is_important = "важн" in text.lower() or "срочно" in text.lower()

            return Meeting(
                title=toolcall.get("topic", "Встреча")[:60],
                date=date_str,
                time=meeting_time,
                description=toolcall.get("summary", ""),
                is_important=is_important
            )
        except Exception as e:
            print(f"ExecuteToolCall error: {e}")
            return results.ErrorResult(str(e))
