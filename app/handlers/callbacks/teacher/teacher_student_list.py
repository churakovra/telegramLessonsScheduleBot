from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.notifiers.telegram_notifier import TelegramNotifier
from app.services.teacher_service import TeacherService
from app.services.user_service import UserService
from app.utils.enums.menu_type import MenuType
from app.utils.exceptions.teacher_exceptions import TeacherStudentsNotFound
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.keyboards.callback_factories.sub_menu import SubMenuCallback
from app.utils.message_template import MessageTemplate

router = Router()


@router.callback_query(SubMenuCallback.filter(F.menu_type == MenuType.TEACHER_STUDENT_LIST))
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
        student_usernames = [student.username for student in students]

        await callback.message.answer(
            text=f"Вот список твоих студентов: \n{"@".join(student_usernames)}"
        )
    except UserNotFoundException as e:
        await callback.message.answer(f"Not enough rights. User {e.data} must have Teacher role, but has {e.role}")
    except TeacherStudentsNotFound as e:
        await callback.message.answer(f"You don't have any student yet")
    finally:
        user_service = UserService(session)
        user, markup = await user_service.get_user_menu(username)
        bot_message = MessageTemplate.get_menu_message(user.username, markup)
        await notifier.send_message(
            bot_message=bot_message,
            receiver_chat_id=callback.message.chat.id
        )

        await callback.answer()
