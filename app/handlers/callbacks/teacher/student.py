from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard import markup_type_by_role
from app.keyboard.builder import MarkupBuilder
from app.keyboard.callback_factories.student import StudentCallback
from app.notifier.telegram_notifier import TelegramNotifier
from app.services.teacher_service import TeacherService
from app.services.user_service import UserService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import ActionType
from app.utils.exceptions.teacher_exceptions import TeacherStudentsNotFound
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.message_template import main_menu_message

router = Router()


@router.callback_query(StudentCallback.filter(F.action == ActionType.CREATE))
async def create(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    teacher_service = TeacherService(session)
    try:
        teacher = await teacher_service.get_teacher(callback.from_user.username)
        await state.update_data(teacher_uuid=teacher.uuid)
        await state.set_state(ScheduleStates.wait_for_teacher_students)
        message = await callback.message.answer(BotStrings.Teacher.TEACHER_STUDENT_ADD)
        await state.update_data(previous_message_id=message.message_id)
    except UserNotFoundException:
        await callback.message.answer(BotStrings.Teacher.NOT_ENOUGH_RIGHTS)
        return
    finally:
        await callback.message.delete()
        await callback.answer()


@router.callback_query(StudentCallback.filter(F.action == ActionType.LIST))
async def list(
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
    except TeacherStudentsNotFound:
        await callback.message.answer("You don't have any student yet")
    finally:
        user_service = UserService(session)
        user = await user_service.get_user(username)
        markup = MarkupBuilder.build(markup_type_by_role[user.role])
        bot_message = main_menu_message(user.username, markup)
        await notifier.send_message(
            bot_message=bot_message, receiver_chat_id=callback.message.chat.id
        )
        await callback.answer()


@router.callback_query(StudentCallback.filter(F.action == ActionType.DELETE))
async def delete(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ScheduleStates.wait_for_student_to_delete)
    await callback.message.delete()
    await callback.message.answer(BotStrings.Teacher.TEACHER_STUDENT_DELETE)
