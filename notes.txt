#Создание KeyboardMarkup
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    time = '14:40'
    button = aiogram.types.InlineKeyboardButton(text=time, callback_data=f'switched day {time}')
    buttons_row1 = [button, button, button]
    buttons_row2 = [button, button, button]
    keyboard_rows = [buttons_row1, buttons_row2]
    markup = aiogram.types.InlineKeyboardMarkup(
        inline_keyboard=keyboard_rows
    )
    await message.answer(text=mt.GREETING.value, reply_markup=markup)