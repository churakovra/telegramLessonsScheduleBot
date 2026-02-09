from aiogram import Dispatcher
from .db_session import DBSessionMiddleware
from .user import UserMiddleware

outer_middlewares = [
    DBSessionMiddleware,
    UserMiddleware,
]

inner_middlewares = []

middlewares_map = {
    "outer": outer_middlewares,
    "inner": inner_middlewares,
}


def register_middlewares(dp: Dispatcher):
    for middleware_type, middlewares in middlewares_map.items():
        updater = (
            dp.update.outer_middleware
            if middleware_type == "outer"
            else dp.update.middleware
        )
        for middleware in middlewares:
            updater(middleware())
