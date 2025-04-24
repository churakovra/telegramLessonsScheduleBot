from aiogram import Dispatcher
from .start import router as start_router
from .new_lesson import router as new_lesson_router
from .callbacks.new_lesson_day_callback import router as new_lesson_callback_router

routers = [
    start_router,
    new_lesson_router,
    new_lesson_callback_router
]

def register_routers(dp: Dispatcher):
    for router in routers:
        dp.include_router(router)