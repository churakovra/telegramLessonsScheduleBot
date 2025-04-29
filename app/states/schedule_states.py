from aiogram.filters.state import StatesGroup, State


class ScheduleStates(StatesGroup):
    wait_for_slots = State()
