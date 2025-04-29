import string
from datetime import datetime, timedelta

from app.models.teacher_slot import Slot
from app.utils.datetime_utils import WEEKDAYS


def parse_slots(mt: str, mf: str) -> list[Slot]:
    raw_mt = [word.strip(string.punctuation) for word in mt.split()]
    res: list[Slot] = list()
    for index, word in enumerate(raw_mt):
        for weekday_index, weekdays in enumerate(WEEKDAYS):
            if word.lower() in weekdays:
                slots_time = list()
                try:
                    for time in raw_mt[index + 1:]:
                        slot_time = datetime.strptime(time, "%H:%M").time()
                        slots_time.append(slot_time)
                except ValueError:
                    break
                finally:
                    today = datetime.today()
                    slot_date = (today + timedelta(days=7 - today.weekday() + weekday_index)).date()
                    day_name = weekdays[0]
                    slot = Slot(
                        teacher=mf,
                        slot_date=slot_date,  # Изменить
                        day_name=day_name,
                        available_time=slots_time
                    )
                    res.append(slot)
    return res
