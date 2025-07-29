from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.utils.enums.menu_type import MenuType
from app.utils.keyboards.callback_factories.sub_menu import SubMenuCallback

router = Router()


@router.callback_query(SubMenuCallback.filter(F.menu_type == MenuType.TEACHER_LESSON_DELETE))
async def handle_callback(
        callback: CallbackQuery,
        state: FSMContext
):
    pass
