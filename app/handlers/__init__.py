from aiogram import Dispatcher

from .callbacks import callback_routers
from .commands import command_routers
from .states import state_routers

routers = []
[routers.append(router) for router in command_routers]
[routers.append(router) for router in callback_routers]
[routers.append(router) for router in state_routers]


def register_routers(dp: Dispatcher):
    [dp.include_router(router) for router in routers]
