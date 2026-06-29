from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message

from app.keyboard.fabric import MarkupData
from app.message.models import BotMessage


async def delete_previous_messages(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    previous_message_id = data.get("previous_message_id")

    if previous_message_id is not None:
        await message.chat.delete_message(message_id=previous_message_id)

    await message.delete()


async def send_next_prompt(
    message: Message,
    state: FSMContext,
    next_state: State,
    prompt_text: str,
    markup: MarkupData | None = None,
) -> Message:
    await state.set_state(next_state)
    msg = BotMessage(text=prompt_text, markup=markup)
    sent_message = await message.answer(**msg.to_aiogram_kwargs())
    await state.update_data(previous_message_id=sent_message.message_id)
    return sent_message
