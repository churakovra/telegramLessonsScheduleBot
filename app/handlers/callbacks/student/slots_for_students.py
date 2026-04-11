from uuid import UUID

from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard.callback_factories.slot import SlotsForStudents
from app.message.models import BotMessage, MarkupData, MessageEnvelope, MessageRecipient
from app.message.utils import slots_to_reply
from app.notifier.producer import MessageProducer
from app.schemas.slot import SlotDTO
from app.schemas.user import UserDTO
from app.services.slot_service import SlotService
from app.services.teacher_service import TeacherService
from app.utils.bot_strings import BotStrings
from app.utils.datetime_utils import full_format_no_sec
from app.utils.enums.bot_values import UserRole

router = Router()


@router.callback_query(SlotsForStudents.filter())
async def handle_callback(
    callback: CallbackQuery,
    callback_data: SlotsForStudents,
    session: AsyncSession,
    user: UserDTO,
    producer: MessageProducer,
):
    slot_uuid = callback_data.uuid_slot
    assigned_slot = await assign_slot(
        session=session, student=user, slot_uuid=slot_uuid
    )
    teacher_service = TeacherService(session=session)
    teacher = await teacher_service.get_teacher_by_uuid(
        teacher_uuid=assigned_slot.uuid_teacher
    )

    slot_time = assigned_slot.dt_start.strftime(full_format_no_sec)
    await notify_student(
        teacher=teacher, student=user, slot_time=slot_time, producer=producer
    )
    await notify_teacher(
        teacher=teacher, student=user, slot_time=slot_time, producer=producer
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
    teacher: UserDTO, student: UserDTO, slot_time: str, producer: MessageProducer
) -> None:
    # Build message with success markup for slot taken
    from app.keyboard.fabric import success_slot_bind
    from app.keyboard.callback_factories.slot import ResendSlotsCallback

    text = BotStrings.Student.SLOTS_ASSIGN_SUCCESS.format(
        teacher=teacher.username, slot_time=slot_time
    )
    markup = success_slot_bind(
        type(
            "Context",
            (),
            {"teacher_uuid": teacher.uuid, "student_chat_id": student.chat_id},
        )()
    )
    message = BotMessage(text=text, markup=markup)

    envelope = MessageEnvelope(
        message=message, recipients=[MessageRecipient(chat_id=student.chat_id)]
    )
    await producer.produce(envelope)


async def notify_teacher(
    teacher: UserDTO, student: UserDTO, slot_time: str, producer: MessageProducer
) -> None:
    # Build notification message for teacher
    text = BotStrings.Teacher.SLOT_IS_TAKEN.format(
        student=student.username, slot_time=slot_time
    )
    message = BotMessage(text=text)

    envelope = MessageEnvelope(
        message=message, recipients=[MessageRecipient(chat_id=teacher.chat_id)]
    )
    await producer.produce(envelope)
