from uuid import UUID

from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.notifier.telegram_notifier import TelegramNotifier
from app.schemas.slot_dto import SlotDTO
from app.schemas.user_dto import UserDTO
from app.services.slot_service import SlotService
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.utils.datetime_utils import full_format_no_sec
from app.utils.enums.bot_values import KeyboardType
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.keyboard.callback_factories.slot import SlotsForStudents
from app.keyboard.builder import MarkupBuilder
from app.keyboard.context import SuccessSlotBindKeyboardContext
from app.utils.message_template import slot_is_taken_message, success_slot_bind_message

router = Router()


@router.callback_query(SlotsForStudents.filter())
async def handle_callback(
    callback: CallbackQuery,
    callback_data: SlotsForStudents,
    session: AsyncSession,
    notifier: TelegramNotifier,
):
    slot_uuid = callback_data.uuid_slot
    student_username = callback.from_user.username
    try:
        student_service = StudentService(session=session)
        student = await student_service.get_student_by_username(
            username=student_username
        )
        assigned_slot = await assign_slot(
            session=session, student=student, slot_uuid=slot_uuid
        )
        teacher_service = TeacherService(session=session)
        teacher = await teacher_service.get_teacher_by_uuid(
            teacher_uuid=assigned_slot.uuid_teacher
        )
    except UserNotFoundException:
        raise ValueError()

    slot_time = assigned_slot.dt_start.strftime(full_format_no_sec)
    await notify_student(
        teacher=teacher, student=student, slot_time=slot_time, notifier=notifier
    )
    await notify_teacher(
        teacher=teacher, student=student, slot_time=slot_time, notifier=notifier
    )

    await callback.message.delete()
    await callback.answer()


async def assign_slot(
    session: AsyncSession,
    student: UserDTO,
    slot_uuid: UUID,
) -> SlotDTO:
    slot_service = SlotService(session=session)
    return await slot_service.assign_slot(
        student_uuid=student.uuid, slot_uuid=slot_uuid
    )


async def notify_student(
    teacher: UserDTO, student: UserDTO, slot_time: str, notifier: TelegramNotifier
) -> None:
    markup_context = SuccessSlotBindKeyboardContext(
        teacher_uuid=teacher.uuid,
        student_chat_id=student.chat_id,
        role=student.role,
        username=teacher.username,
    )
    markup = MarkupBuilder.build(KeyboardType.SUCCESS_SLOT_BIND, markup_context)
    bot_message = success_slot_bind_message(
        teacher=teacher.username, slot_time=slot_time, markup=markup
    )
    await notifier.send_message(
        bot_message=bot_message, receiver_chat_id=student.chat_id
    )


async def notify_teacher(
    teacher: UserDTO, student: UserDTO, slot_time: str, notifier: TelegramNotifier
) -> None:
    notify_teacher_message = slot_is_taken_message(
        student_username=student.username, slot_time=slot_time
    )
    await notifier.send_message(
        bot_message=notify_teacher_message, receiver_chat_id=teacher.chat_id
    )
