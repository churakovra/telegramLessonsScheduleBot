from aiogram.filters.state import StatesGroup, State


class ScheduleStates(StatesGroup):
    wait_for_teacher_username = State() # add Teacher status to user
    wait_for_slots = State() # wait for teacher slots & start to process them
    wait_for_confirmation = State() # wait for teacher confirmation is bot parsed slots correctly
    wait_for_teacher_students = State() # wait student tg usernames for bind them to teacher
    wait_for_student_to_delete = State() # wait student tg usernames for unbind them to teacher
    wait_for_teacher_lesson_label = State() # wait for new lesson label
    wait_for_teacher_lesson_duration = State() # wait for new lesson duration
    wait_for_teacher_lesson_price = State() # wait for new lesson price
    wait_for_lesson_update = State() # wait for new lesson label/duration/price