from dataclasses import dataclass


@dataclass
class Meeting:
    title: str = ""
    date: str = ""
    time: str = ""
    description: str = ""
    is_important: bool = False
    id: int = None

    def short_repr(self):
        return self.title
