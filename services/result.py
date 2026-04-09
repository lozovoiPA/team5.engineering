from data.entities.meeting import Meeting


class Result:
    def __init__(self, _type):
        self._type = _type


class ErrorResult(Result):
    def __init__(self, error_text):
        super().__init__("ErrorResult")
        self.error_text = error_text


class MeetingsCreated(Result):
    def __init__(self):
        super().__init__("meetings_created")


class TaskSchedulerSuccess(Result):
    def __init__(self):
        super().__init__("notification_planned")


class MeetingsRetrieved(Result):
    def __init__(self, meetings):
        super().__init__("meetings_retrieved")
        self.meetings: list[Meeting] = meetings


class MeetingsDeleted(Result):
    def __init__(self):
        super().__init__("meetings_deleted")


class MeetingsUpdated(Result):
    def __init__(self):
        super().__init__("meetings_updated")
