import calendar
from datetime import date
from io import StringIO
from uuid import UUID

from tabulate import tabulate

from app.schemas.lesson import LessonDTO
from app.schemas.slot import SlotDTO
from app.schemas.student import StudentDTO
from app.schemas.user import UserDTO
from app.utils.datetime_utils import WEEKDAYS
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def slots_to_reply(slots: list[SlotDTO]) -> str:
    response = ""
    slots_temp = dict[str, tuple[set[str], list[str]]]()
    for slot in slots:
        # Get number of day in week depending on date
        weekday = calendar.weekday(
            slot.dt_start.year, slot.dt_start.month, slot.dt_start.day
        )
        # Get day label; [2]-label in WEEKDAYS on russian
        label = WEEKDAYS[weekday][2]
        # Date (without time) in str format
        sdate = slot.dt_start.strftime("%d.%m.%y")
        # Time (without date) in str format
        time = slot.dt_start.strftime("%H:%M")
        if label not in slots_temp:
            slots_temp[label] = (set(), [])
        slots_temp[label][0].add(sdate)
        slots_temp[label][1].append(time)

    for label, slot_info in slots_temp.items():
        response += (
            f"📅: {label}, {slot_info[0].pop()}\n🕐: {', '.join(slot_info[1])}\n\n"
        )
    return response


def get_student_info(student: StudentDTO, **kwargs) -> str:
    lessons = kwargs["lessons"]
    name = " ".join([student.firstname, student.lastname or ""])
    username = student.username
    student_lessons = ", ".join([lesson.label for lesson in lessons])
    return f"Имя: {name}\nЛогин: {username}\nПредметы: {student_lessons}"


def get_slot_info(slot: SlotDTO) -> str:
    slot_dt = slot.dt_start
    studnet = slot.uuid_student
    response = f"Slot\nДата/Время: {slot_dt}\n Ученик: {studnet or 'Нет'}"
    return response


def get_lesson_info(lesson: LessonDTO) -> str:
    label = f"*{lesson.label}*"
    duration = f"Длительность {lesson.duration} мин"
    price = f"Стоимость {lesson.price} руб"
    return f"{label}\n{duration}\n{price}"


def get_slots_schedule_reply(
    slots: list[SlotDTO], lessons: dict[UUID, LessonDTO], students: list[UserDTO]
) -> str:
    student_map = {s.uuid: s for s in students}

    response = StringIO()
    current_day: date | None = None
    day_slots: list[dict[str, str]] = []
    lessons_cnt = 0
    day_earning = 0
    week_lessons_cnt = 0
    week_earning = 0

    def write_day_summary():
        if day_slots:
            rows = {
                "time": [s["time"] for s in day_slots],
                "student": [s["student"] for s in day_slots],
                "price": [s["price"] for s in day_slots],
            }
            response.write(f"{tabulate(rows, headers=['Время', 'Ученик', 'Цена'])}\n")
            response.write(f"Уроков {lessons_cnt}, за день {day_earning}\n\n")

    for slot in slots:
        slot_date = slot.dt_start.date()
        slot_time = slot.dt_start.time()

        if slot_date != current_day:
            if current_day is not None:
                write_day_summary()
                week_lessons_cnt += lessons_cnt
                week_earning += day_earning

            current_day = slot_date
            week_day_num = current_day.isocalendar().weekday
            weekday = WEEKDAYS[week_day_num][2]
            response.write(f"{weekday} {current_day}\n")
            day_slots.clear()
            lessons_cnt = 0
            day_earning = 0

        if not slot.uuid_student:
            day_slots.append({"time": str(slot_time), "student": "", "price": ""})
            continue

        if slot.uuid_student not in lessons:
            logger.error(
                f"Student {slot.uuid_student} has no lesson, but somehow spotted slot {slot.uuid}"
            )
            continue

        student = student_map.get(slot.uuid_student)
        if not student:
            logger.error(f"Student {slot.uuid_student} not found in students list")
            continue

        lesson = lessons[slot.uuid_student]
        day_slots.append(
            {
                "time": str(slot_time),
                "student": student.username,
                "price": str(lesson.price),
            }
        )

        lessons_cnt += 1
        day_earning += lesson.price

    write_day_summary()
    week_lessons_cnt += lessons_cnt
    week_earning += day_earning
    response.write(f"Итого: ЗАНЯТИЙ {week_lessons_cnt} ДОХОД {week_earning}")

    return response.getvalue()
