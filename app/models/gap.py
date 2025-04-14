from dataclasses import dataclass
from datetime import datetime


@dataclass
class Gap:
    number: int #может пригодится в будущем нумеровка урока
    datetime_start: datetime
    datetime_end: datetime
