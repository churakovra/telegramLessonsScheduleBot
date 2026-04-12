# TODO delete getting user in every place in handlers except middleware
from aiogram import F, Router
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard.callback_factories.slot import (
    SlotCreateCallback,
    SlotDeleteCallback,
    SlotInfoCallback,
    SlotListCallback,
    SlotsUpdateCallback,
)
from app.keyboard.fabric import (
    cancel_markup,
    slot_buttons,
    specify_week,
    teacher_main_menu,
)
from app.message.models import BotMessage, MarkupData
from app.message.utils import get_slot_info, get_slots_schedule_reply
from app.services.lesson_service import LessonService
from app.services.slot_service import SlotService
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import WeekFlag
from app.utils.exceptions.lesson_exceptions import LessonsNotFoundException
from app.utils.exceptions.slot_exceptions import SlotsNotFoundException
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.callback_query(
    or_f(
        SlotCreateCallback.filter(F.week_flag.is_(None)),
        SlotListCallback.filter(F.week_flag.is_(None)),
        SlotsUpdateCallback.filter(F.week_flag.is_(None)),
    )
)
async def specify_week_handler(
    callback: CallbackQuery,
    callback_data: SlotCreateCallback | SlotListCallback,
) -> None:
    markup = specify_week(type("Context", (), {"callback_cls": type(callback_data)})())
    message = BotMessage(text=BotStrings.Common.SPECIFY_WEEK, markup=markup)
    await callback.message.answer(**message.to_aiogram_kwargs())
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

    markup = cancel_markup()
    message = BotMessage(text=BotStrings.Teacher.SLOTS_ADD, markup=markup)
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()
    logger.info("Add slot flow has been started")


@router.callback_query(
    SlotsUpdateCallback.filter(F.week_flag.in_([WeekFlag.CURRENT, WeekFlag.NEXT]))
)
async def update(
    callback: CallbackQuery,
    callback_data: SlotsUpdateCallback,
    state: FSMContext,
):
    await state.set_state(ScheduleStates.wait_for_slots_update)
    await state.update_data(week_flag=callback_data.week_flag)

    markup = cancel_markup()
    message = BotMessage(text=BotStrings.Teacher.SLOTS_ADD, markup=markup)
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


@router.callback_query(
    SlotListCallback.filter(F.week_flag.in_([WeekFlag.CURRENT, WeekFlag.NEXT]))
)
async def list_slots(
    callback: CallbackQuery, callback_data: SlotListCallback, session: AsyncSession
) -> None:
    logger.debug("In SlotList")
    teacher_service = TeacherService(session)
    slot_service = SlotService(session)
    try:
        teacher = await teacher_service.get_teacher(callback.from_user.username)
        slots = await slot_service.get_slots(teacher.uuid, callback_data.week_flag)
        markup = slot_buttons(type("Context", (), {"slots": slots})())
        message = BotMessage(text=BotStrings.Teacher.SLOTS_LIST, markup=markup)
    except UserNotFoundException as e:
        error_msg = f"Not enough rights. User {e.data} must have Teacher role."
        logger.error(error_msg, e)
        markup = cancel_markup()
        message = BotMessage(text=BotStrings.Common.NOT_ENOUGH_RIGHTS, markup=markup)
    except SlotsNotFoundException as e:
        logger.error(e)
        markup = cancel_markup()
        message = BotMessage(text=BotStrings.Teacher.SLOTS_NOT_FOUND, markup=markup)
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


@router.callback_query(SlotInfoCallback.filter())
async def info(
    callback: CallbackQuery, callback_data: SlotInfoCallback, session: AsyncSession
) -> None:
    slot_service = SlotService(session)
    slot = await slot_service.get_slot(callback_data.uuid)
    text = get_slot_info(slot)
    message = BotMessage(text=text)
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


@router.callback_query(SlotDeleteCallback.filter())
async def delete(
    callback: CallbackQuery, callback_data: SlotDeleteCallback, session: AsyncSession
):
    # TODO потестить. Посмотреть, будет ли работать cascade delete.
    slot_service = SlotService(session)
    await slot_service.delete_slot(callback_data.uuid)

    markup = teacher_main_menu()
    message = BotMessage(text=BotStrings.Teacher.SLOT_DELETE_SUCCESS, markup=markup)
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


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

        text = get_slots_schedule_reply(slots, lessons, students)
        message = BotMessage(text=text)
        await callback.message.answer(**message.to_aiogram_kwargs())
    except LessonsNotFoundException:
        pass
    except SlotsNotFoundException:
        message = BotMessage(
            text="Окошек не найдено. Добавь их с помощью Меню -> Расписание -> Добавить окошки"
        )
        await callback.message.answer(**message.to_aiogram_kwargs())
    finally:
        await callback.answer()
