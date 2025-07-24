from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.notifiers.telegram_notifier import TelegramNotifier
from app.services.teacher_service import TeacherService
from app.services.user_service import UserService
from app.states.schedule_states import ScheduleStates
from app.utils.enums.menu_type import MenuType
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.keyboards.callback_factories.sub_menu import SubMenuCallback
from app.utils.bot_strings import BotStrings
from app.utils.message_template import MessageTemplate

router = Router()


@router.callback_query(SubMenuCallback.filter(F.menu_type == MenuType.TEACHER_SLOT_ADD))
async def handle_callback(
        callback: CallbackQuery,
        session: AsyncSession,
        state: FSMContext,
        notifier: TelegramNotifier
):
    teacher_service = TeacherService(session)
    try:
        teacher = await teacher_service.get_teacher(callback.from_user.username)

        sent_message = await callback.message.answer(f"Привет, {callback.from_user.first_name}, я жду твои окошки")
        await state.set_state(ScheduleStates.wait_for_slots)
        await state.update_data(previous_message_id=sent_message.message_id)
        await state.update_data(teacher_uuid=teacher.uuid)

    except UserNotFoundException:
        await callback.message.answer(BotStrings.NOT_ENOUGH_RIGHTS)
        user_service = UserService(session)
        user, markup = await user_service.get_user_menu(callback.message.from_user.username)
        bot_message = MessageTemplate.get_menu_message(user.username, markup)
        await notifier.send_message(
            bot_message=bot_message,
            receiver_chat_id=callback.message.chat.id
        )
        return
    finally:
        await callback.message.delete()
        await callback.answer()
