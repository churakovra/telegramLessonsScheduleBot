from uuid import UUID

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.keyboards.callback_factories.send_slots import SendSlotsCallback


def get_send_slots_markup(teacher_uuid: UUID):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Отправить",
        callback_data=SendSlotsCallback(teacher_uuid=teacher_uuid)
    )
    return builder.as_markup()