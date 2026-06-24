from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboard.callback_factories.slot import SlotsForStudents
from app.keyboard.fabric import success_slot_bind
from app.notifier.sender import MessageSender
from app.schemas.user import UserDTO
from app.services.container import Services
from app.utils.bot_strings import BotStrings
from app.utils.datetime_utils import full_format_no_sec

router = Router()


@router.callback_query(SlotsForStudents.filter())
async def handle_callback(
    callback: CallbackQuery,
    callback_data: SlotsForStudents,
    services: Services,
    user: UserDTO,
    sender: MessageSender,
) -> None:
    assigned_slot = await services.slot.assign_slot(
        student_uuid=user.uuid, slot_uuid=callback_data.uuid_slot
    )
    teacher = await services.teacher.get_teacher_by_uuid(
        teacher_uuid=assigned_slot.uuid_teacher
    )

    slot_time = assigned_slot.dt_start.strftime(full_format_no_sec)

    # Notify student
    text = BotStrings.Student.SLOTS_ASSIGN_SUCCESS.format(
        teacher=teacher.username, slot_time=slot_time
    )
    markup = success_slot_bind(
        teacher_uuid=teacher.uuid,
        student_chat_id=user.chat_id,
    )
    await sender.send_to_chat(chat_id=user.chat_id, text=text, markup=markup)

    # Notify teacher
    teacher_text = BotStrings.Teacher.SLOT_IS_TAKEN.format(
        student=user.username, slot_time=slot_time
    )
    await sender.send_to_chat(chat_id=teacher.chat_id, text=teacher_text)

    await callback.message.delete()
    await callback.answer()
