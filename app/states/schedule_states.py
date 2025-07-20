from aiogram.filters.state import StatesGroup, State


class ScheduleStates(StatesGroup):
    wait_for_teacher_username = State()
    wait_for_slots = State()
    wait_for_confirmation = State()
    new_slots_ready = State()
    wait_for_teacher_students = State()
    wait_for_teacher_lesson_label = State()
    wait_for_teacher_lesson_duration = State()
    wait_for_teacher_lesson_price = State()
    create_lesson = State()
