from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard.builder import MarkupBuilder
from app.keyboard.callback_factories.student import StudentCallback, StudentList
from app.keyboard.context import StudentOperationKeyboardContext
from app.services.lesson_service import LessonService
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import ActionType, KeyboardType
from app.utils.exceptions.teacher_exceptions import TeacherStudentsNotFound
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.callback_query(StudentCallback.filter(F.action == ActionType.CREATE))
async def create(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext
) -> None:
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
async def list(callback: CallbackQuery, session: AsyncSession) -> None:
    teacher_service = TeacherService(session)
    student_service = StudentService(session)
    username = callback.from_user.username
    try:
        markup = None
        teacher = await teacher_service.get_teacher(username)
        students = await student_service.get_students_by_teacher_uuid(teacher.uuid)
        message_text = BotStrings.Teacher.TEACHER_STUDENTS_LIST
        markup_context = StudentOperationKeyboardContext(students, StudentList)
        markup = MarkupBuilder.build(KeyboardType.STUDENT_OPERATION, markup_context)
    except UserNotFoundException as e:
        error_msg = f"Not enough rights. User {e.data} must have Teacher role."
        logger.error(error_msg, e)
        message_text = BotStrings.Common.NOT_ENOUGH_RIGHTS
    except TeacherStudentsNotFound as e:
        logger.error(e)
        message_text = BotStrings.Teacher.TEACHER_STUDENTS_NOT_FOUND

    await callback.message.answer(text=message_text, reply_markup=markup)
    await callback.answer()


@router.callback_query(StudentList.filter())
async def get_student_info(
    callback: CallbackQuery, callback_data: StudentList, session: AsyncSession
):
    student_service = StudentService(session)
    lesson_service = LessonService(session)
    student = await student_service.get_student_by_uuid(callback_data.uuid)
    lessons = await lesson_service.get_student_lessons(student.uuid)
    response_msg = await student_service.get_student_info(student, lessons)
    await callback.message.answer(response_msg)
    await callback.answer()


# TODO add student update


@router.callback_query(
    StudentCallback.filter(F.action == ActionType.DELETE)
)  # TODO rework. send approve keyboard; delete on StudentDelete callback.
async def delete(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ScheduleStates.wait_for_student_to_delete)
    await callback.message.delete()
    await callback.message.answer(BotStrings.Teacher.TEACHER_STUDENT_DELETE)
