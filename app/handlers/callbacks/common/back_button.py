from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.slot_service import SlotService
from app.services.user_service import UserService
from app.utils.exceptions.teacher_exceptions import TeacherStudentsNotFound
from app.utils.exceptions.user_exceptions import (
    UserNotFoundException,
    UserUnknownRoleException,
)
from app.utils.keyboards.callback_factories.back import Back
from app.utils.keyboards.markup_builder import MarkupBuilder
from app.utils.message_template import MessageTemplate

router = Router()


@router.callback_query(Back.filter())
async def handle_callback(
    callback: CallbackQuery, callback_data: Back, session: AsyncSession
):
    parent_keyboard = callback_data.parent_keyboard
    try:
        match parent_keyboard:
            case "menu_keyboard":  # TODO Вынести в ENUM
                username = callback.from_user.username
                user_service = UserService(session)
                user = await user_service.get_user(username)
                markup = MarkupBuilder.main_menu_markup(user.role)
                message = MessageTemplate.main_menu_message(user.username, markup)
                await callback.message.answer(
                    text=message.message_text, reply_markup=message.reply_markup
                )
            case "days_for_students":  # TODO Вынести в ENUM
                if callback_data.teacher_uuid is None:
                    raise ValueError("callback_data.teacher_uuid is None")
                teacher_uuid = callback_data.teacher_uuid
                slot_service = SlotService(session)
                slots = await slot_service.get_free_slots(teacher_uuid)
                markup = MarkupBuilder.days_for_students_markup(slots, teacher_uuid)
                await callback.message.answer(
                    text=callback.message.text, reply_markup=markup
                )
            case _:
                raise ValueError("Unknown parent_keyboard value")
    except (UserNotFoundException, UserUnknownRoleException) as e:
        await callback.message.answer(e.message)
    except TeacherStudentsNotFound as e:
        await callback.message.answer(e.message)
    finally:
        await callback.message.delete()
        await callback.answer()
