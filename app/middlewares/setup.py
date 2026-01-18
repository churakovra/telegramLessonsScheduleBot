from aiogram import Dispatcher

from app.middlewares.db_session import DBSessionMiddleware
from app.middlewares.validate_teacher import ValidateTeacherMiddleware


def setup_middlewares(dp: Dispatcher):
    dp.update.middleware(DBSessionMiddleware())
    # dp.update.middleware(ValidateTeacherMiddleware())
