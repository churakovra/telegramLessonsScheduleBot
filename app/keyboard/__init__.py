from app.utils.enums.bot_values import KeyboardType, UserRole
from app.keyboard.fabric import (
    admin_main_menu,
    admin_sub_menu_temp,
    confirm_deletion,
    days_for_students,
    is_slots_correct_markup,
    lesson_operation,
    send_slots,
    slots_for_students,
    specify_week,
    specs_to_update,
    student_main_menu,
    student_sub_menu_slot,
    student_sub_menu_teacher,
    success_slot_bind,
    teacher_main_menu,
    teacher_sub_menu_lesson,
    teacher_sub_menu_slot,
    teacher_sub_menu_student,
)

keyboard_registry: dict = {
    KeyboardType.TEACHER_MAIN: teacher_main_menu,
    KeyboardType.TEACHER_SUB_STUDENT: teacher_sub_menu_student,
    KeyboardType.TEACHER_SUB_SLOT: teacher_sub_menu_slot,
    KeyboardType.TEACHER_SUB_LESSON: teacher_sub_menu_lesson,
    KeyboardType.STUDENT_MAIN: student_main_menu,
    KeyboardType.STUDENT_SUB_TEACHER: student_sub_menu_teacher,
    KeyboardType.STUDENT_SUB_SLOT: student_sub_menu_slot,
    KeyboardType.ADMIN_MAIN: admin_main_menu,
    KeyboardType.ADMIN_SUB_TEMP: admin_sub_menu_temp,
    KeyboardType.IS_SLOTS_CORRECT: is_slots_correct_markup,
    KeyboardType.SEND_SLOTS: send_slots,
    KeyboardType.DAYS_FOR_STUDENTS: days_for_students,
    KeyboardType.SLOTS_FOR_STUDENTS: slots_for_students,
    KeyboardType.SUCCESS_SLOT_BIND: success_slot_bind,
    KeyboardType.SPECIFY_WEEK: specify_week,
    KeyboardType.LESSONS_OPERATION: lesson_operation,
    KeyboardType.CONFIRM_DELETION: confirm_deletion,
    KeyboardType.SPECS_TO_UPDATE: specs_to_update,
}


markup_type_by_role = {
    UserRole.TEACHER: KeyboardType.TEACHER_MAIN,
    UserRole.STUDENT: KeyboardType.STUDENT_MAIN,
    UserRole.ADMIN: KeyboardType.ADMIN_MAIN,
}
