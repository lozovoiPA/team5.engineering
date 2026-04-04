from dataclasses import dataclass


@dataclass
class Meeting:
    title: str
    date: str
    time: str
    description: str = ""
    is_important: bool = False
    id: int = 0

    def short_repr(self):
        return self.title