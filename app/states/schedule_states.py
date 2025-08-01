from aiogram.filters.state import StatesGroup, State


class ScheduleStates(StatesGroup):
    wait_for_teacher_username = State() # стейт для добавления юзеру статуса Teacher
    wait_for_slots = State() # стейт для получения и обработки окошек от преподавателя
    wait_for_confirmation = State() # стейт, ожидающий подтверждения преподавателем корректности парсинга окошек
    wait_for_teacher_students = State() # стейт, ожидающий ввода преподавателем никнеймов студентов для привязки
    wait_for_teacher_lesson_label = State() # стейт, ожидающий ввода преподавателем названия нового предмета
    wait_for_teacher_lesson_duration = State() # стейт, ожидающий ввода преподавателем продолжительности нового предмета
    wait_for_teacher_lesson_price = State() # стейт, ожидающий ввода преподавателем стоимости нового предмета
    wait_for_student_to_delete = State() # стейт, ожидающий ввода преподавателем никнейма студента для отвязки