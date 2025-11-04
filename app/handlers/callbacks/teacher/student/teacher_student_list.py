from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.notifiers.telegram_notifier import TelegramNotifier
from app.services.teacher_service import TeacherService
from app.services.user_service import UserService
from app.utils.enums.menu_type import MenuType
from app.utils.exceptions.teacher_exceptions import TeacherStudentsNotFound
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.keyboards.callback_factories.menu import SubMenu
from app.utils.keyboards.markup_builder import MarkupBuilder
from app.utils.message_template import MessageTemplate

router = Router()


@router.callback_query(
    SubMenu.filter(F.menu_type == MenuType.TEACHER_STUDENT_LIST)
)
async def handle_callback(
    callback: CallbackQuery,
    session: AsyncSession,
    notifier: TelegramNotifier,
):
    username = callback.from_user.username
    await callback.message.delete()
    teacher_service = TeacherService(session)

    try:
        teacher = await teacher_service.get_teacher(username)
        students = await teacher_service.get_students(teacher.uuid)
        student_usernames = [f"@{student.username}" for student in students]

        await callback.message.answer(
            text=f"Вот список твоих студентов: \n{'\n'.join(student_usernames)}"
        )
    except UserNotFoundException as e:
        await callback.message.answer(
            f"Not enough rights. User {e.data} must have Teacher role, but has {e.role}"
        )
    except TeacherStudentsNotFound as e:
        await callback.message.answer("You don't have any student yet")
    finally:
        user_service = UserService(session)
        user = await user_service.get_user(username)
        markup = MarkupBuilder.main_menu_markup(user.role)
        bot_message = MessageTemplate.main_menu_message(user.username, markup)
        await notifier.send_message(
            bot_message=bot_message, receiver_chat_id=callback.message.chat.id
        )

        await callback.answer()
