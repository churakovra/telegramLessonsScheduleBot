from aiogram import F, Router
from aiogram.filters import and_f, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.keyboard.callback_factories.slot import (
    SlotCreateCallback,
    SlotDeleteCallback,
    SlotInfoCallback,
    SlotListCallback,
    SlotsClearCallback,
    SlotsUpdateCallback,
)
from app.keyboard.fabric import (
    cancel_markup,
    confirm_action,
    listed_slots_actions,
    specify_week,
    teacher_main_menu,
)
from app.message.models import BotMessage
from app.message.utils import get_slot_info, get_slots_schedule_reply, slots_to_reply
from app.services.container import Services
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
    callback_data: SlotCreateCallback | SlotListCallback | SlotsUpdateCallback,
) -> None:
    callback_cls = type(callback_data)
    markup = specify_week(
        current_week_callback=callback_cls(week_flag=WeekFlag.CURRENT).pack(),
        next_week_callback=callback_cls(week_flag=WeekFlag.NEXT).pack(),
    )
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
    callback: CallbackQuery, callback_data: SlotListCallback, services: Services
) -> None:
    try:
        teacher = await services.teacher.get_teacher(callback.from_user.username)
        slots = await services.slot.get_slots(teacher.uuid, callback_data.week_flag)
        markup = listed_slots_actions(week_flag=callback_data.week_flag)
        message = BotMessage(
            text=f"{BotStrings.Teacher.SLOTS_LIST}\n\n{slots_to_reply(slots)}",
            markup=markup,
        )
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
    callback: CallbackQuery, callback_data: SlotInfoCallback, services: Services
) -> None:
    slot = await services.slot.get_slot(callback_data.uuid)
    text = get_slot_info(slot)
    message = BotMessage(text=text)
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


@router.callback_query(
        SlotsClearCallback.filter(~F.confirmed)
)
async def confirm(
    callback: CallbackQuery,
    callback_data: SlotsClearCallback,
):
    message = BotMessage(
        text=BotStrings.Menu.CONFIRM,
        markup=confirm_action(callback_data=callback_data),
    )
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()

@router.callback_query(
    and_f(
        SlotsClearCallback.filter(F.week_flag.in_([WeekFlag.CURRENT, WeekFlag.NEXT])),
        SlotsClearCallback.filter(F.confirmed.is_(True)),
    )
)
async def clear_slots(
    callback: CallbackQuery,
    callback_data: SlotsClearCallback,
    services: Services,
) -> None:
    try:
        teacher = await services.teacher.get_teacher(callback.from_user.username)
        deleted_count = await services.slot.delete_free_slots(
            teacher.uuid,
            callback_data.week_flag,
        )
        markup = teacher_main_menu()
        message = BotMessage(
            text=BotStrings.Teacher.SLOTS_CLEAR_SUCCESS.format(count=deleted_count),
            markup=markup,
        )
    except UserNotFoundException as e:
        error_msg = f"Not enough rights. User {e.data} must have Teacher role."
        logger.error(error_msg, e)
        markup = cancel_markup()
        message = BotMessage(text=BotStrings.Common.NOT_ENOUGH_RIGHTS, markup=markup)
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


@router.callback_query(SlotDeleteCallback.filter())
async def delete(
    callback: CallbackQuery, callback_data: SlotDeleteCallback, services: Services
):
    # TODO потестить. Посмотреть, будет ли работать cascade delete.
    await services.slot.delete_slot(callback_data.uuid)

    markup = teacher_main_menu()
    message = BotMessage(text=BotStrings.Teacher.SLOT_DELETE_SUCCESS, markup=markup)
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


@router.callback_query(SlotListCallback.filter(F.week_flag.in_([WeekFlag.UNKNOWN])))
async def statistics(
    callback: CallbackQuery,
    callback_data: SlotListCallback,
    services: Services,
):
    try:
        teacher = await services.teacher.get_teacher(callback.from_user.username)
        slots = await services.slot.get_slots(teacher.uuid, callback_data.week_flag)
        lessons = await services.lesson.get_students_lessons_by_slots(slots)
        students = [
            await services.student.get_student_by_uuid(slot.uuid_student)
            for slot in slots
            if slot.uuid_student
        ]

        text = get_slots_schedule_reply(slots, lessons, students)
        message = BotMessage(text=text)
        await callback.message.answer(**message.to_aiogram_kwargs())
    except LessonsNotFoundException:
        message = BotMessage(text=BotStrings.Teacher.SLOTS_NOT_FOUND)
        await callback.message.answer(**message.to_aiogram_kwargs())
    except SlotsNotFoundException:
        message = BotMessage(
            text=BotStrings.Teacher.SLOTS_NOT_FOUND
        )
        await callback.message.answer(**message.to_aiogram_kwargs())
    finally:
        await callback.answer()
