from aiogram import Dispatcher

from app.handlers.commands.new_schedule import router as new_schedule
from app.handlers.states.wait_for_slots import router as wait_for_slots
from app.handlers.callbacks.slots_correct import router as slots_correct
from app.handlers.callbacks.slots_incorrect import router as slots_incorrect
from app.handlers.callbacks.new_lesson_day_callback import router as new_lesson_callback_router
from app.handlers.commands.new_lesson import router as new_lesson_router
from app.handlers.commands.start import router as start_router

routers = [
    start_router,
    wait_for_slots,
    slots_correct,
    slots_incorrect,
    new_schedule,
    new_lesson_router,
    new_lesson_callback_router
]


def register_routers(dp: Dispatcher):
    for router in routers:
        dp.include_router(router)
