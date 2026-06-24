from aiogram import Dispatcher

from .db_session import DBSessionMiddleware
from .sender_injection import SenderInjectionMiddleware
from .services import ServicesMiddleware
from .user import UserMiddleware

outer_middlewares = [
    DBSessionMiddleware,
    ServicesMiddleware,
    UserMiddleware,
    SenderInjectionMiddleware,
]

inner_middlewares = []  # type: ignore

middlewares_map = {
    "outer": outer_middlewares,
    "inner": inner_middlewares,
}


def register_middlewares(dp: Dispatcher) -> None:
    for middleware_type, middlewares in middlewares_map.items():
        updater = (
            dp.update.outer_middleware
            if middleware_type == "outer"
            else dp.update.middleware
        )
        for middleware in middlewares:
            updater(middleware())
