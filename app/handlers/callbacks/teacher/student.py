from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard.builder import MarkupBuilder
from app.keyboard.callback_factories.student import (
    StudentAttachCallback,
    StudentCreateCallback,
    StudentDeleteCallback,
    StudentDetachCallback,
    StudentInfoCallback,
    StudentListCallback,
)
from app.keyboard.context import (
    ConfirmDeletionKeyboardContext,
    EntitiesListKeyboardContext,
    EntityOperationsKeyboardContext,
    LessonsToAttachKeyboardContext,
)
from app.services.lesson_service import LessonService
from app.services.slot_service import SlotService
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.states.schedule_states import ScheduleStates
from app.utils import message_template as mt
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import EntityType, KeyboardType
from app.utils.exceptions.teacher_exceptions import TeacherStudentsNotFound
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.callback_query(StudentCreateCallback.filter())
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


@router.callback_query(StudentListCallback.filter())
async def list(callback: CallbackQuery, session: AsyncSession) -> None:
    teacher_service = TeacherService(session)
    student_service = StudentService(session)
    username = callback.from_user.username
    try:
        markup = None
        teacher = await teacher_service.get_teacher(username)
        students = await student_service.get_students_by_teacher_uuid(teacher.uuid)
        message_text = BotStrings.Teacher.TEACHER_STUDENTS_LIST
        markup_context = EntitiesListKeyboardContext(students, EntityType.STUDENT)
        markup = MarkupBuilder.build(KeyboardType.ENTITIES_LIST, markup_context)
    except UserNotFoundException as e:
        error_msg = f"Not enough rights. User {e.data} must have Teacher role."
        logger.error(error_msg, e)
        message_text = BotStrings.Common.NOT_ENOUGH_RIGHTS
    except TeacherStudentsNotFound as e:
        logger.error(e)
        message_text = BotStrings.Teacher.TEACHER_STUDENTS_NOT_FOUND
    await callback.message.answer(text=message_text, reply_markup=markup)
    await callback.answer()


@router.callback_query(StudentInfoCallback.filter())
async def get_student_info(
    callback: CallbackQuery, callback_data: StudentInfoCallback, session: AsyncSession
):
    student_service = StudentService(session)
    lesson_service = LessonService(session)
    student = await student_service.get_student_by_uuid(callback_data.uuid)
    lessons = await lesson_service.get_student_lessons(student.uuid)
    response_msg = await student_service.get_student_info(student, lessons)
    markup_context = EntityOperationsKeyboardContext(
        uuid=callback_data.uuid, entity_type=EntityType.STUDENT
    )
    markup = MarkupBuilder.build(KeyboardType.ENTITY_OPERATIONS, markup_context)
    await callback.message.answer(text=response_msg, reply_markup=markup)
    await callback.answer()


@router.callback_query(StudentDeleteCallback.filter(F.confirmed == False))
async def request_delete_confirmation(
    callback: CallbackQuery, callback_data: StudentDeleteCallback
):
    markup_context = ConfirmDeletionKeyboardContext(
        StudentDeleteCallback, callback_data
    )
    markup = MarkupBuilder.build(KeyboardType.CONFIRM_DELETION, markup_context)
    await callback.message.answer(**mt.confirm_student_deletion(markup))
    await callback.answer()


@router.callback_query(StudentDeleteCallback.filter(F.confirmed == True))
async def delete_lesson(
    callback: CallbackQuery, callback_data: StudentDeleteCallback, session: AsyncSession
):
    teacher_service = TeacherService(session)
    slot_service = SlotService(session)
    teacher = await teacher_service.get_teacher(callback.from_user.username)
    student_uuid = callback_data.uuid
    await teacher_service._detach_student(
        teacher_uuid=teacher.uuid, student_uuid=student_uuid
    )
    await slot_service.delete_slots_attached_to_student(student_uuid)
    await callback.message.answer(**mt.student_deletion_success())
    await callback.answer()


@router.callback_query(StudentAttachCallback.filter(F.lesson_uuid == None))
async def list_lessons_to_attach(callback: CallbackQuery, callback_data: StudentAttachCallback, session: AsyncSession):
    student_service = StudentService(session)
    lesson_service = LessonService(session)
    username = callback.from_user.username
    
    student = await student_service.get_student_by_username(username)
    lessons = await lesson_service.get_lessons_to_attach(student)
    makrup_context = LessonsToAttachKeyboardContext(student.uuid, lessons)
    markup = MakrupBuilder.build(KeyboardType.LESSONS_TO_ATTACH, markup_context)
    pass


@router.callback_query(StudentAttachCallback.filter(F.lesson_uuid != None))
async def attach(callback: CallbackQuery, callback_data: StudentAttachCallback, session: AsyncSession): ...



@router.callback_query(StudentDetachCallback.filter(F.lesson_uuid == None))
async def list_lessons_to_detach(callback: CallbackQuery, callback_data: StudentDetachCallback): ...


@router.callback_query(StudentDetachCallback.filter(F.lesson_uuid != None))
async def detach(callback: CallbackQuery, callback_data: StudentDetachCallback): ...