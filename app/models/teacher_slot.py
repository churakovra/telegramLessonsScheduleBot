from dataclasses import dataclass
from datetime import date, time


@dataclass
class Slot:
    teacher: str
    slot_date: date
    day_name: str
    available_time: list[time]
