from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard.builder import MarkupBuilder
from app.keyboard.callback_factories.slot import SlotCallback, SlotsList, SlotsUpdate
from app.keyboard.context import SpecifyWeekKeyboardContext
from app.services.lesson_service import LessonService
from app.services.slot_service import SlotService
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import ActionType, KeyboardType, WeekFlag
from app.utils.exceptions.lesson_exceptions import LessonsNotFoundException
from app.utils.exceptions.slot_exceptions import SlotsNotFoundException
from app.utils.logger import setup_logger
from app.utils.message_template import specify_week_message

router = Router()
logger = setup_logger(__name__)


@router.callback_query(SlotCallback.filter(F.action == ActionType.CREATE))
async def create(
    callback: CallbackQuery,
    state: FSMContext,
):
    await state.set_state(ScheduleStates.wait_for_slots)
    await state.update_data(week_flag=WeekFlag.NEXT)
    await state.update_data(operation_type=ActionType.CREATE)
    await callback.message.answer(BotStrings.Teacher.SLOTS_ADD)
    await callback.answer()
    logger.info("Add slot flow has been started")



@router.callback_query(SlotCallback.filter(F.action == ActionType.UPDATE))
async def update(callback: CallbackQuery):
    markup_context = SpecifyWeekKeyboardContext(SlotsUpdate)
    markup = MarkupBuilder.build(KeyboardType.SPECIFY_WEEK, markup_context)
    message = specify_week_message(markup)
    await callback.message.answer(**message)
    await callback.answer()


@router.callback_query(SlotsUpdate.filter())
async def update_slots(
    callback: CallbackQuery, callback_data: SlotsUpdate, state: FSMContext
):
    await state.set_state(ScheduleStates.wait_for_slots)
    await state.update_data(week_flag=callback_data.week_flag)
    await state.update_data(operation_type=ActionType.UPDATE)
    await callback.message.answer(BotStrings.Teacher.SLOTS_ADD)
    await callback.answer()



@router.callback_query(SlotCallback.filter(F.action == ActionType.LIST))
async def list(callback: CallbackQuery) -> None:
    markup_context = SpecifyWeekKeyboardContext(SlotsList)
    markup = MarkupBuilder.build(KeyboardType.SPECIFY_WEEK, markup_context)
    message = specify_week_message(markup=markup)
    await callback.message.answer(**message)
    await callback.answer()


@router.callback_query(SlotsList.filter())
async def list_slots(
    callback: CallbackQuery,
    callback_data: SlotsList,
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
    except LessonsNotFoundException:
        pass
    except SlotsNotFoundException:
        await callback.message.answer(
            text="Окошек не найдено. Добавь их с помощью Меню -> Расписание -> Добавить окошки"
        )
    finally:
        await callback.answer()
