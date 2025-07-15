from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config.logger import setup_logger
from app.utils.bot_strings import BotStrings

logger = setup_logger()

def get_sub_menu_markup(sub_menu_type: str):
    builder = InlineKeyboardBuilder()
    logger.debug(f"in get_sub_menu_markup, sub_menu_type={sub_menu_type}")
    match sub_menu_type:
        case BotStrings.CALLBACK_GROUP_TEACHER_STUDENT:
            callbacks = {
                "Добавить ученика": BotStrings.CALLBACK_GROUP_TEACHER_STUDENT_ADD,
                "Изменить ученика": BotStrings.CALLBACK_GROUP_TEACHER_STUDENT_EDIT,
                "Получить список учеников": BotStrings.CALLBACK_GROUP_TEACHER_STUDENT_LIST,
                "Удалить ученика": BotStrings.CALLBACK_GROUP_TEACHER_STUDENT_DELETE
            }
        case BotStrings.CALLBACK_GROUP_TEACHER_SLOT:
            callbacks = {
                "Добавить окошки": BotStrings.CALLBACK_GROUP_TEACHER_SLOT_ADD,
                "Изменить окошки": BotStrings.CALLBACK_GROUP_TEACHER_SLOT_EDIT,
                "Записать ученика в окошко": BotStrings.CALLBACK_GROUP_TEACHER_SLOT_SPOT,
                "Получить список окошек": BotStrings.CALLBACK_GROUP_TEACHER_SLOT_LIST,
                "Удалить окошко": BotStrings.CALLBACK_GROUP_TEACHER_SLOT_DELETE
            }
        case BotStrings.CALLBACK_GROUP_TEACHER_LESSON:
            callbacks = {
                "Добавить предмет": BotStrings.CALLBACK_GROUP_TEACHER_LESSON_ADD,
                "Изменить предмет": BotStrings.CALLBACK_GROUP_TEACHER_LESSON_EDIT,
                "Получить список предметов": BotStrings.CALLBACK_GROUP_TEACHER_LESSON_LIST,
                "Удалить предмет": BotStrings.CALLBACK_GROUP_TEACHER_LESSON_DELETE
            }
        case _:
            raise ValueError(f"Wrong sub_menu_type {sub_menu_type}")
    for name, value in callbacks.items():
        builder.add(
            InlineKeyboardButton(
                text=name,
                callback_data=value
            )
        )
        logger.debug(f"get_sub_menu_markup: name={name}; callback_data={value}")
    builder.adjust(1)
    return builder.as_markup()