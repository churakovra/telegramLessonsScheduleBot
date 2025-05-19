from aiogram.filters.state import StatesGroup, State


class ScheduleStates(StatesGroup):
    wait_for_teacher_username = State()
    wait_for_slots = State()
    wait_for_confirmation = State()
    wait_slots_send_to_students = State()
