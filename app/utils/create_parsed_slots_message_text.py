from app.models.teacher_slot import Slot


def create_parsed_slots_message_text(parsed_lessons: list[Slot]) -> str:
    slot_message = ""
    for slot in parsed_lessons:
        slot_message += (f"📅: {slot.day_name}, {slot.slot_date}\n"
                         f"🕐: {", ".join(map(lambda slot_time: slot_time.strftime("%H:%M"), slot.available_time))}\n\n")
    slot_message += "Верно?"
    return slot_message
