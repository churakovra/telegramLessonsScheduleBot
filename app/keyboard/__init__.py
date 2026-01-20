from app.keyboard.callback_factories.lesson import LessonDeleteCallback, LessonUpdateCallback
from app.keyboard.callback_factories.slot import SlotDeleteCallback, SlotUpdateCallback
from app.keyboard.callback_factories.student import StudentAttachCallback, StudentDeleteCallback, StudentDetachCallback, StudentUpdateCallback
from app.keyboard.fabric import (
    admin_main_menu,
    admin_sub_menu_temp,
    confirm_deletion,
    days_for_students,
    entities_list,
    entity_operations,
    is_slots_correct_markup,
    lessons_to_attach,
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
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import EntityType, KeyboardType, UserRole

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
    KeyboardType.CONFIRM_DELETION: confirm_deletion,
    KeyboardType.SPECS_TO_UPDATE: specs_to_update,
    KeyboardType.ENTITIES_LIST: entities_list,
    KeyboardType.ENTITY_OPERATIONS: entity_operations,
    KeyboardType.LESSONS_TO_ATTACH: lessons_to_attach
}


markup_type_by_role = {
    UserRole.TEACHER: KeyboardType.TEACHER_MAIN,
    UserRole.STUDENT: KeyboardType.STUDENT_MAIN,
    UserRole.ADMIN: KeyboardType.ADMIN_MAIN,
}


operations = {
        EntityType.STUDENT: {
            BotStrings.Menu.ATTACH: StudentAttachCallback,
            BotStrings.Menu.DETACH: StudentDetachCallback,
            BotStrings.Menu.DELETE: StudentDeleteCallback,
        },
        EntityType.LESSON: {
            BotStrings.Menu.UPDATE: LessonUpdateCallback,
            BotStrings.Menu.DELETE: LessonDeleteCallback,
        },
        EntityType.SLOT: {
            BotStrings.Menu.UPDATE: SlotUpdateCallback,
            BotStrings.Menu.DELETE: SlotDeleteCallback,
        },
    }
