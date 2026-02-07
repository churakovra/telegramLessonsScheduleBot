from aiogram import Dispatcher

from .callbacks import callback_routers
from .commands import command_routers
from .states import state_routers

routers = []
routers.extend(command_routers)
routers.extend(callback_routers)
routers.extend(state_routers)


def register_routers(dp: Dispatcher):
    [dp.include_router(router) for router in routers]
