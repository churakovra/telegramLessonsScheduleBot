from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.lesson_service import LessonService
from app.services.slot_service import SlotService
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.utils.enums.menu_type import MenuType
from app.utils.exceptions.lesson_exceptions import LessonsNotFoundException
from app.utils.exceptions.slot_exceptions import SlotsNotFoundException
from app.utils.keyboard.callback_factories.menu import SubMenu
from app.utils.keyboard.callback_factories.slots import ListSlots
from app.utils.keyboard.builder import MarkupBuilder
from app.utils.message_template import MessageTemplate

router = Router()


@router.callback_query(SubMenu.filter(F.menu_type == MenuType.TEACHER_SLOT_LIST))
async def on_teacher_slot_list(callback: CallbackQuery):
    markup = MarkupBuilder.specify_week_markup(callback_data=ListSlots)
    message = MessageTemplate.specify_week_message(markup=markup)
    await callback.message.answer(
        text=message.message_text, reply_markup=message.reply_markup
    )
    await callback.answer()


@router.callback_query(ListSlots.filter())
async def handle_callback(
    callback: CallbackQuery,
    callback_data: ListSlots,
    session: AsyncSession,
):
    teacher_service = TeacherService(session)
    slot_service = SlotService(session)
    lesson_service = LessonService(session)
    student_service = StudentService(session)
    try:
        teacher = await teacher_service.get_teacher(callback.from_user.username)
        slots = await slot_service.get_slots(teacher.uuid, callback_data.week_flag)
        lessons = await lesson_service.get_students_lessons_by_slots(slots)
        students = [
            await student_service.get_student_by_uuid(slot.uuid_student)
            for slot in slots
            if slot.uuid_student
        ]
        slots_schedule = await slot_service.get_slots_schedule_reply(
            slots, lessons, students
        )
        await callback.message.answer(
            text=f"`{slots_schedule}`", parse_mode="MarkdownV2"
        )
    except LessonsNotFoundException as e:
        pass
    except SlotsNotFoundException as e:
        await callback.message.answer(
            text="Окошек не найдено. Добавь их с помощью Меню -> Расписание -> Добавить окошки"
        )
    finally:
        await callback.answer()
