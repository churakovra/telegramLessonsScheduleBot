from aiogram.types import InlineKeyboardMarkup

from app.schemas.bot_message import BotMessage
from app.schemas.slot_dto import SlotDTO
from app.services.slot_service import SlotService
from app.utils.bot_strings import BotStrings


class MessageTemplate:
    @staticmethod
    def main_menu_message(username: str, markup: InlineKeyboardMarkup) -> BotMessage:
        return BotMessage(
            message_text=BotStrings.Common.MENU.format(user=username),
            reply_markup=markup,
        )

    @staticmethod
    async def slots_added_for_student_message(slots: list[SlotDTO], markup: InlineKeyboardMarkup):
        return BotMessage(
            message_text=f"{BotStrings.Student.SLOTS_ADDED}\n\n{await SlotService.get_parsed_slots_reply(slots)}",
            reply_markup=markup,
        )
        
    @staticmethod
    async def slots_updated_for_student_message(slots: list[SlotDTO], markup: InlineKeyboardMarkup):
        return BotMessage(
            message_text=f"{BotStrings.Student.SLOTS_UPDATED}\n\n{await SlotService.get_parsed_slots_reply(slots)}",
            reply_markup=markup,
        )

    @staticmethod
    def slot_is_taken_message(student_username: str, slot_time: str) -> BotMessage:
        return BotMessage(
            message_text=BotStrings.Teacher.SLOT_IS_TAKEN.format(
                student=student_username,
                slot_time=slot_time,
            ),
            reply_markup=None,
        )

    @staticmethod
    def success_slot_bind_message(
        teacher: str, slot_time: str, markup: InlineKeyboardMarkup
    ) -> BotMessage:
        return BotMessage(
            message_text=BotStrings.Student.SLOTS_ASSIGN_SUCCESS.format(
                teacher=teacher,
                slot_time=slot_time,
            ),
            reply_markup=markup,
        )

    @staticmethod
    def specify_week_message(
        markup: InlineKeyboardMarkup
    ) -> BotMessage:
        return BotMessage(
            message_text=BotStrings.Common.SPECIFY_WEEK,
            reply_markup=markup
        )
