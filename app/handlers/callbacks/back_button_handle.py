from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboards.slots_for_students_markup import BackPressed
from app.use_cases.pop_message import pop_message_use_case

router = Router()


@router.callback_query(BackPressed.filter())
async def back_pressed_handle(
        callback: CallbackQuery,
        callback_data: BackPressed,
        **kwargs
):
    notifier = kwargs["notifier"]
    chat_id = callback_data.chat_id
    message = pop_message_use_case(chat_id, notifier)
    await callback.message.edit_reply_markup(reply_markup=message.reply_markup)
    await callback.answer()
