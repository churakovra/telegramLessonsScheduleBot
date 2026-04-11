from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard.callback_factories.student import (
    StudentAssignCallback,
    StudentCreateCallback,
    StudentDeleteCallback,
    StudentDetachCallback,
    StudentInfoCallback,
    StudentListCallback,
)
from app.message.models import BotMessage, MarkupData
from app.services.lesson_service import LessonService
from app.services.slot_service import SlotService
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import EntityType
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

        message_context = context.Common(
            text=BotStrings.Teacher.TEACHER_STUDENT_ADD,
            markup_context=CancelKeyboardContext(),
        )
        message = await callback.message.answer(
            **message_builder.build(message_context)
        )
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
    message_context: context.AbstractBotMessageContext
    try:
        teacher = await teacher_service.get_teacher(username)
        students = await student_service.get_students_by_teacher_uuid(teacher.uuid)
        logger.debug(f"teacher {teacher}")
        logger.debug(f"teacher.uuid {teacher.uuid}")
        logger.debug(f"students {students}")
        message_context = context.EntitiesList(students, EntityType.STUDENT)
    except UserNotFoundException as e:
        # TODO send error msg; send MainMenu msg via notifier
        error_msg = f"Not enough rights. User {e.data} must have Teacher role."
        logger.error(error_msg, e)
        message_context = context.Common(
            BotStrings.Common.NOT_ENOUGH_RIGHTS,
            MainMenuKeyboardContext(UserRole.TEACHER),
        )
    except TeacherStudentsNotFound as e:
        logger.error(e)
        message_context = context.Common(
            BotStrings.Teacher.TEACHER_STUDENTS_NOT_FOUND,
            MainMenuKeyboardContext(UserRole.TEACHER),
        )
    await callback.message.answer(**message_builder.build(message_context))
    await callback.answer()


@router.callback_query(StudentInfoCallback.filter())
async def info(
    callback: CallbackQuery, callback_data: StudentInfoCallback, session: AsyncSession
) -> None:
    student_service = StudentService(session)
    lesson_service = LessonService(session)
    student = await student_service.get_student_by_uuid(callback_data.uuid)
    lessons = await lesson_service.get_student_lessons(student.uuid)
    message_context = context.StudentInfo(student, lessons)
    message_context = BotMessage.entity_info(student, lessons=lessons)
    await callback.message.answer(**message_builder.build(message_context))
    await callback.answer()


@router.callback_query(StudentDeleteCallback.filter(F.confirmed.is_(False)))
async def request_delete_confirmation(
    callback: CallbackQuery, callback_data: StudentDeleteCallback
) -> None:
    message_context = context.ConfirmOperation(StudentDeleteCallback, callback_data)
    await callback.message.answer(**message_builder.build(message_context))
    await callback.answer()


@router.callback_query(StudentDeleteCallback.filter(F.confirmed.is_(True)))
async def delete_student(
    callback: CallbackQuery, callback_data: StudentDeleteCallback, session: AsyncSession
) -> None:
    teacher_service = TeacherService(session)
    slot_service = SlotService(session)
    teacher = await teacher_service.get_teacher(callback.from_user.username)
    student_uuid = callback_data.uuid
    await teacher_service._detach_student(
        teacher_uuid=teacher.uuid, student_uuid=student_uuid
    )
    await slot_service.delete_slots_attached_to_student(student_uuid)
    message_context = context.Common(
        text=BotStrings.Teacher.TEACHER_STUDENT_DELETE_SUCCESS,
        markup_context=MainMenuKeyboardContext(UserRole.TEACHER),
    )
    await callback.message.answer(**message_builder.build(message_context))
    await callback.answer()


@router.callback_query(StudentAssignCallback.filter(F.id_lesson.is_(None)))
async def list_lessons_to_attach(
    callback: CallbackQuery, callback_data: StudentAssignCallback, session: AsyncSession
) -> None:
    teacher_service = TeacherService(session)
    lesson_service = LessonService(session)
    username = callback.from_user.username
    teacher = await teacher_service.get_teacher(username)
    lessons = await lesson_service.get_lessons_to_attach(
        student_uuid=callback_data.uuid, teacher_uuid=teacher.uuid
    )
    message_context = context.StudentAssign(callback_data.uuid, lessons)
    await callback.message.answer(**message_builder.build(message_context))
    await callback.answer()


@router.callback_query(StudentAssignCallback.filter(F.id_lesson.is_not(None)))
async def attach(
    callback: CallbackQuery, callback_data: StudentAssignCallback, session: AsyncSession
) -> None:
    teacher_service = TeacherService(session)
    lesson_service = LessonService(session)
    teacher = await teacher_service.get_teacher(callback.from_user.username)
    lesson = await lesson_service.get_lesson_by_id(callback_data.id_lesson)
    await lesson_service.attach_lesson(callback_data.uuid, teacher.uuid, lesson.uuid)
    message_context = context.Common(
        text=BotStrings.Teacher.STUDENT_ATTACH_SUCCESS,
        markup_context=SubMenuKeyboardContext(UserRole.TEACHER, EntityType.STUDENT),
    )
    await callback.message.answer(**message_builder.build(message_context))
    await callback.answer()


@router.callback_query(StudentDetachCallback.filter(F.id_lesson.is_(None)))
async def list_lessons_to_detach(
    callback: CallbackQuery, callback_data: StudentDetachCallback, session: AsyncSession
) -> None:
    teacher_service = TeacherService(session)
    lesson_service = LessonService(session)
    username = callback.from_user.username
    teacher = await teacher_service.get_teacher(username)
    lessons = await lesson_service.get_lessons_to_detach(
        student_uuid=callback_data.uuid, teacher_uuid=teacher.uuid
    )
    message_context = context.StudentAssign(callback_data.uuid, lessons)
    await callback.message.answer(**message_builder.build(message_context))
    await callback.answer()


@router.callback_query(StudentDetachCallback.filter(F.id_lesson.is_not(None)))
async def detach(
    callback: CallbackQuery, callback_data: StudentDetachCallback, session: AsyncSession
) -> None:
    teacher_service = TeacherService(session)
    lesson_service = LessonService(session)
    teacher = await teacher_service.get_teacher(callback.from_user.username)
    lesson = await lesson_service.get_lesson_by_id(callback_data.id_lesson)
    await lesson_service.detach_specific_lesson(
        callback_data.uuid, teacher.uuid, lesson.uuid
    )
    message_context = context.Common(
        text=BotStrings.Teacher.STUDENT_ATTACH_SUCCESS,
        markup_context=SubMenuKeyboardContext(UserRole.TEACHER, EntityType.STUDENT),
    )
    await callback.message.answer(**message_builder.build(message_context))
    await callback.answer()
