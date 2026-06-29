from datetime import datetime

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.keyboard.callback_factories.recurrence import (
    RecurrenceConfirmCallback,
    RecurrenceCreateCallback,
    RecurrenceDayCallback,
    RecurrenceDeleteCallback,
    RecurrenceListCallback,
)
from app.keyboard.fabric import (
    cancel_markup,
    recurrence_confirm_menu,
    recurrence_days_menu,
    recurrence_rules_buttons,
    teacher_recurrence_menu,
)
from app.message.models import BotMessage
from app.schemas.user import UserDTO
from app.services.container import Services
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.datetime_utils import day_format, time_format_HM

router = Router()


@router.callback_query(RecurrenceListCallback.filter())
async def list_recurrence_rules(
    callback: CallbackQuery,
    services: Services,
    user: UserDTO,
) -> None:
    rules = await services.recurrence.get_teacher_rules(user.uuid)
    if not rules:
        message = BotMessage(
            text=BotStrings.Teacher.RECURRENCE_RULES_NOT_FOUND,
            markup=teacher_recurrence_menu(),
        )
    else:
        message = BotMessage(
            text=BotStrings.Teacher.RECURRENCE_RULES,
            markup=recurrence_rules_buttons(rules=rules),
        )
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


@router.callback_query(RecurrenceCreateCallback.filter())
async def create_recurrence(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.answer(
        **BotMessage(
            text=BotStrings.Teacher.RECURRENCE_SELECT_DAY,
            markup=recurrence_days_menu(),
        ).to_aiogram_kwargs()
    )
    await callback.answer()


@router.callback_query(RecurrenceDayCallback.filter())
async def select_recurrence_day(
    callback: CallbackQuery,
    callback_data: RecurrenceDayCallback,
    state: FSMContext,
) -> None:
    await state.update_data(day_of_week=callback_data.day_of_week)
    await state.set_state(ScheduleStates.wait_for_recurrence_start_time)
    await callback.message.answer(
        **BotMessage(
            text=BotStrings.Teacher.RECURRENCE_START_TIME,
            markup=cancel_markup(),
        ).to_aiogram_kwargs()
    )
    await callback.answer()


@router.message(ScheduleStates.wait_for_recurrence_start_time)
async def wait_for_recurrence_start_time(
    message: Message,
    state: FSMContext,
) -> None:
    value = _parse_time(message.text)
    if value is None:
        await message.answer(**BotMessage(text=BotStrings.Errors.INVALID_INPUT).to_aiogram_kwargs())
        return
    await state.update_data(time_start=value)
    await state.set_state(ScheduleStates.wait_for_recurrence_end_time)
    await message.answer(
        **BotMessage(
            text=BotStrings.Teacher.RECURRENCE_END_TIME,
            markup=cancel_markup(),
        ).to_aiogram_kwargs()
    )


@router.message(ScheduleStates.wait_for_recurrence_end_time)
async def wait_for_recurrence_end_time(message: Message, state: FSMContext) -> None:
    value = _parse_time(message.text)
    if value is None:
        await message.answer(**BotMessage(text=BotStrings.Errors.INVALID_INPUT).to_aiogram_kwargs())
        return
    await state.update_data(time_end=value)
    await state.set_state(ScheduleStates.wait_for_recurrence_duration)
    await message.answer(
        **BotMessage(
            text=BotStrings.Teacher.RECURRENCE_DURATION,
            markup=cancel_markup(),
        ).to_aiogram_kwargs()
    )


@router.message(ScheduleStates.wait_for_recurrence_duration)
async def wait_for_recurrence_duration(message: Message, state: FSMContext) -> None:
    try:
        duration = int((message.text or "").strip())
    except ValueError:
        await message.answer(**BotMessage(text=BotStrings.Errors.INVALID_INPUT).to_aiogram_kwargs())
        return
    await state.update_data(slot_duration=duration)
    await state.set_state(ScheduleStates.wait_for_recurrence_start_date)
    await message.answer(
        **BotMessage(
            text=BotStrings.Teacher.RECURRENCE_START_DATE,
            markup=cancel_markup(),
        ).to_aiogram_kwargs()
    )


@router.message(ScheduleStates.wait_for_recurrence_start_date)
async def wait_for_recurrence_start_date(message: Message, state: FSMContext) -> None:
    value = _parse_date(message.text)
    if value is None:
        await message.answer(**BotMessage(text=BotStrings.Errors.INVALID_INPUT).to_aiogram_kwargs())
        return
    await state.update_data(date_start=value)
    await state.set_state(ScheduleStates.wait_for_recurrence_end_date)
    await message.answer(
        **BotMessage(
            text=BotStrings.Teacher.RECURRENCE_END_DATE,
            markup=cancel_markup(),
        ).to_aiogram_kwargs()
    )


@router.message(ScheduleStates.wait_for_recurrence_end_date)
async def wait_for_recurrence_end_date(message: Message, state: FSMContext) -> None:
    value = _parse_date(message.text)
    if value is None:
        await message.answer(**BotMessage(text=BotStrings.Errors.INVALID_INPUT).to_aiogram_kwargs())
        return
    await state.update_data(date_end=value)
    data = await state.get_data()
    summary = _format_recurrence_summary(data)
    await message.answer(
        **BotMessage(
            text=BotStrings.Teacher.RECURRENCE_CONFIRM.format(summary=summary),
            markup=recurrence_confirm_menu(),
        ).to_aiogram_kwargs()
    )


@router.callback_query(RecurrenceConfirmCallback.filter())
async def confirm_recurrence(
    callback: CallbackQuery,
    callback_data: RecurrenceConfirmCallback,
    state: FSMContext,
    services: Services,
    user: UserDTO,
) -> None:
    if not callback_data.confirm:
        await state.clear()
        await callback.message.answer(
            **BotMessage(
                text=BotStrings.Common.MENU,
                markup=teacher_recurrence_menu(),
            ).to_aiogram_kwargs()
        )
        await callback.answer()
        return

    data = await state.get_data()
    await services.recurrence.create_rule(
        teacher_uuid=user.uuid,
        day_of_week=data["day_of_week"],
        time_start=data["time_start"],
        time_end=data["time_end"],
        slot_duration=data["slot_duration"],
        date_start=data["date_start"],
        date_end=data["date_end"],
    )
    await state.clear()
    await callback.message.answer(
        **BotMessage(
            text=BotStrings.Teacher.RECURRENCE_CREATE_SUCCESS,
            markup=teacher_recurrence_menu(),
        ).to_aiogram_kwargs()
    )
    await callback.answer()


@router.callback_query(RecurrenceDeleteCallback.filter())
async def delete_recurrence_rule(
    callback: CallbackQuery,
    callback_data: RecurrenceDeleteCallback,
    services: Services,
) -> None:
    await services.recurrence.delete_rule(callback_data.uuid)
    await callback.message.answer(
        **BotMessage(
            text=BotStrings.Teacher.RECURRENCE_DELETE_SUCCESS,
            markup=teacher_recurrence_menu(),
        ).to_aiogram_kwargs()
    )
    await callback.answer()


def _parse_time(value: str | None):
    if not value:
        return None
    try:
        return datetime.strptime(value.strip(), time_format_HM).time()
    except ValueError:
        return None


def _parse_date(value: str | None):
    if not value:
        return None
    try:
        return datetime.strptime(value.strip(), day_format).date()
    except ValueError:
        return None


def _format_recurrence_summary(data: dict) -> str:
    return BotStrings.Teacher.RECURRENCE_SUMMARY.format(
        day=BotStrings.Common.WEEKDAY_LABELS[data["day_of_week"]],
        time_start=f"{data['time_start']:%H:%M}",
        time_end=f"{data['time_end']:%H:%M}",
        duration=data["slot_duration"],
        date_start=f"{data['date_start']:%d.%m.%Y}",
        date_end=f"{data['date_end']:%d.%m.%Y}",
    )
