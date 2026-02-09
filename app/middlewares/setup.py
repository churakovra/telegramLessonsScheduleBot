from aiogram import Dispatcher

from app.middlewares.db_session import DBSessionMiddleware


def setup_middlewares(dp: Dispatcher):
    dp.update.middleware(DBSessionMiddleware())
    # dp.update.middleware(ValidateTeacherMiddleware())
