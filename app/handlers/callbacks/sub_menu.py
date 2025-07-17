from aiogram import Router
from aiogram.types import CallbackQuery

from app.utils.keyboards.callback_factories.sub_menu import SubMenuCallback

router = Router()


@router.callback_query(SubMenuCallback.filter())
async def handle_callback(
        callback: CallbackQuery,
        callback_data: SubMenuCallback
):
    pass
