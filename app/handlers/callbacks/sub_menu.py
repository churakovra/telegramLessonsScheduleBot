from aiogram import Router
from aiogram.types import CallbackQuery

from app.utils.keyboards.sub_menu_markup import SubMenuCallback

router = Router()
@router.callback_query(SubMenuCallback.filter())
async def handle_callback(
        callback: CallbackQuery,
        callback_data: SubMenuCallback
):
    pass