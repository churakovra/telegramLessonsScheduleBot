from aiogram import F, Router
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard.builder import MarkupBuilder
from app.keyboard.callback_factories.slot import (
    SlotCreateCallback,
    SlotInfoCallback,
    SlotListCallback,
    SlotUpdateCallback,
)
from app.keyboard.context import (
    EntitiesListKeyboardContext,
    EntityOperationsKeyboardContext,
    SpecifyWeekKeyboardContext,
)
from app.services.lesson_service import LessonService
from app.services.slot_service import SlotService
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import EntityType, KeyboardType, WeekFlag
from app.utils.exceptions.lesson_exceptions import LessonsNotFoundException
from app.utils.exceptions.slot_exceptions import SlotsNotFoundException
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.logger import setup_logger
from app.utils import message_template as mt

router = Router()
logger = setup_logger(__name__)


@router.callback_query(
    or_f(
        SlotCreateCallback.filter(F.week_flag.is_(None)),
        SlotListCallback.filter(F.week_flag.is_(None)),
    )
)
async def specify_week(
    callback: CallbackQuery, callback_data: SlotCreateCallback | SlotListCallback
) -> None:
    markup_context = SpecifyWeekKeyboardContext(type(callback_data))
    markup = MarkupBuilder.build(KeyboardType.SPECIFY_WEEK, markup_context)
    message = mt.specify_week_message(markup=markup)
    await callback.message.answer(**message)
    await callback.answer()


@router.callback_query(
    SlotCreateCallback.filter(F.week_flag.in_([WeekFlag.CURRENT, WeekFlag.NEXT]))
)
async def create(
    callback: CallbackQuery,
    callback_data: SlotCreateCallback,
    state: FSMContext,
):
    logger.debug("In SlotCreate")
    await state.set_state(ScheduleStates.wait_for_slots)
    await state.update_data(week_flag=callback_data.week_flag)
    markup = MarkupBuilder.build(KeyboardType.CANCEL)
    await callback.message.answer(
        text=BotStrings.Teacher.SLOTS_ADD, reply_markup=markup
    )
    await callback.answer()
    logger.info("Add slot flow has been started")


@router.callback_query(
    SlotListCallback.filter(F.week_flag.in_([WeekFlag.CURRENT, WeekFlag.NEXT]))
)
async def list(
    callback: CallbackQuery, callback_data: SlotListCallback, session: AsyncSession
) -> None:
    logger.debug("In SlotList")
    teacher_service = TeacherService(session)
    slot_service = SlotService(session)
    try:
        markup = None
        teacher = await teacher_service.get_teacher(callback.from_user.username)
        slots = await slot_service.get_slots(teacher.uuid, callback_data.week_flag)
        markup_context = EntitiesListKeyboardContext(slots, EntityType.SLOT)
        markup = MarkupBuilder.build(KeyboardType.ENTITIES_LIST, markup_context)
        message_text = BotStrings.Teacher.SLOTS_LIST
    except UserNotFoundException as e:
        error_msg = f"Not enough rights. User {e.data} must have Teacher role."
        logger.error(error_msg, e)
        markup = MarkupBuilder.build(KeyboardType.CANCEL)
        message_text = BotStrings.Common.NOT_ENOUGH_RIGHTS
    except SlotsNotFoundException as e:
        logger.error(e)
        markup = MarkupBuilder.build(KeyboardType.CANCEL)
        message_text = BotStrings.Teacher.SLOTS_NOT_FOUND
    await callback.message.answer(text=message_text, reply_markup=markup)
    await callback.answer()


@router.callback_query(SlotInfoCallback.filter())
async def info(
    callback: CallbackQuery, callback_data: SlotInfoCallback, session: AsyncSession
) -> None:
    # TODO add slot info str; add slot update callback; slot delete callback handlers
    slot_service = SlotService(session)
    slot = await slot_service.get_slot(callback_data.uuid)
    markup_context = EntityOperationsKeyboardContext(
        callback_data.uuid, EntityType.SLOT
    )
    markup = MarkupBuilder.build(KeyboardType.ENTITY_OPERATIONS, markup_context)
    message_text = slot_service.get_slot_info_response(slot)
    await callback.message.answer(**mt.slot_info(message_text, markup))
    await callback.answer()


@router.callback_query(SlotUpdateCallback.filter())
async def update(
    callback: CallbackQuery, callback_data: SlotUpdateCallback, session: AsyncSession
) -> None:
    pass


@router.callback_query(SlotListCallback.filter(F.week_flag.in_([WeekFlag.UNKNOWN])))
async def statistics(
    callback: CallbackQuery,
    callback_data: SlotListCallback,
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
