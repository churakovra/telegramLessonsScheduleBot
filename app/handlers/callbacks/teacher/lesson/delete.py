from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.utils.enums.menu_type import MenuType
from app.utils.keyboards.callback_factories.menu import SubMenu
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.callback_query(SubMenu.filter(F.menu_type == MenuType.TEACHER_LESSON_DELETE))
async def handle_callback(
        callback: CallbackQuery,
        state: FSMContext
):
    pass
