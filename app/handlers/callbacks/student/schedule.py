from datetime import UTC, datetime, timedelta

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.keyboard.callback_factories.reschedule import (
    StudentRescheduleCallback,
    StudentRescheduleConfirmCallback,
)
from app.keyboard.callback_factories.schedule import (
    StudentScheduleCallback,
    StudentSlotCancelCallback,
    StudentWeeklyScheduleCallback,
)
from app.keyboard.fabric import (
    cancel_markup,
    reschedule_confirm_menu,
    student_main_menu,
    student_schedule_menu,
)
from app.message.models import BotMessage
from app.notifier.sender import MessageSender
from app.schemas.slot import SlotDTO
from app.schemas.user import UserDTO
from app.services.container import Services
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.datetime_utils import day_format, full_format_no_sec, time_format_HM

router = Router()


@router.callback_query(StudentScheduleCallback.filter())
async def show_schedule(
    callback: CallbackQuery,
    services: Services,
    user: UserDTO,
) -> None:
    now = datetime.now(UTC).astimezone()
    start_at = (now - timedelta(days=now.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    end_at = start_at + timedelta(days=14)
    slots = await services.slot.get_student_booked_slots(user.uuid, start_at, end_at)

    if not slots:
        message = BotMessage(
            text=BotStrings.Student.SCHEDULE_EMPTY,
            markup=student_main_menu(),
        )
    else:
        text = await _format_schedule(slots, services, user)
        message = BotMessage(text=text, markup=student_schedule_menu(slots=slots))

    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


@router.callback_query(StudentWeeklyScheduleCallback.filter())
async def show_weekly_schedule(
    callback: CallbackQuery,
    services: Services,
    user: UserDTO,
) -> None:
    text = await services.statistics.get_weekly_summary(user.uuid)
    await callback.message.answer(
        **BotMessage(
            text=text,
            markup=student_main_menu(),
        ).to_aiogram_kwargs()
    )
    await callback.answer()


@router.callback_query(StudentSlotCancelCallback.filter())
async def cancel_slot(
    callback: CallbackQuery,
    callback_data: StudentSlotCancelCallback,
    services: Services,
    user: UserDTO,
    sender: MessageSender,
) -> None:
    slot = await services.slot.unassign_slot(user.uuid, callback_data.uuid_slot)
    teacher = await services.teacher.get_teacher_by_uuid(slot.uuid_teacher)
    slot_time = slot.dt_start.strftime(full_format_no_sec)

    await sender.send_to_chat(
        chat_id=teacher.chat_id,
        text=BotStrings.Teacher.SLOT_CANCELLED_BY_STUDENT.format(
            student=user.username,
            slot_time=slot_time,
        ),
    )
    await callback.message.answer(
        **BotMessage(
            text=BotStrings.Student.SLOT_CANCEL_SUCCESS,
            markup=student_main_menu(),
        ).to_aiogram_kwargs()
    )
    await callback.answer()


@router.callback_query(StudentRescheduleCallback.filter())
async def request_reschedule(
    callback: CallbackQuery,
    callback_data: StudentRescheduleCallback,
    state: FSMContext,
) -> None:
    await state.clear()
    await state.update_data(reschedule_slot_uuid=callback_data.slot_uuid)
    await state.set_state(ScheduleStates.wait_for_reschedule_date)
    await callback.message.answer(
        **BotMessage(
            text=BotStrings.Student.RESCHEDULE_DATE,
            markup=cancel_markup(),
        ).to_aiogram_kwargs()
    )
    await callback.answer()


@router.message(ScheduleStates.wait_for_reschedule_date)
async def wait_for_reschedule_date(message: Message, state: FSMContext) -> None:
    value = _parse_date(message.text)
    if value is None:
        await message.answer(
            **BotMessage(text=BotStrings.Errors.INVALID_INPUT).to_aiogram_kwargs()
        )
        return
    await state.update_data(requested_date=value)
    await state.set_state(ScheduleStates.wait_for_reschedule_time)
    await message.answer(
        **BotMessage(
            text=BotStrings.Student.RESCHEDULE_TIME,
            markup=cancel_markup(),
        ).to_aiogram_kwargs()
    )


@router.message(ScheduleStates.wait_for_reschedule_time)
async def wait_for_reschedule_time(message: Message, state: FSMContext) -> None:
    value = _parse_time(message.text)
    if value is None:
        await message.answer(
            **BotMessage(text=BotStrings.Errors.INVALID_INPUT).to_aiogram_kwargs()
        )
        return
    await state.update_data(requested_time=value)
    data = await state.get_data()
    new_time = f"{data['requested_date']:%d.%m.%Y} {value:%H:%M}"
    await message.answer(
        **BotMessage(
            text=BotStrings.Student.RESCHEDULE_CONFIRM.format(new_time=new_time),
            markup=reschedule_confirm_menu(),
        ).to_aiogram_kwargs()
    )


@router.callback_query(StudentRescheduleConfirmCallback.filter())
async def confirm_reschedule(
    callback: CallbackQuery,
    callback_data: StudentRescheduleConfirmCallback,
    state: FSMContext,
    services: Services,
    user: UserDTO,
    sender: MessageSender,
) -> None:
    if not callback_data.confirm:
        await state.clear()
        await callback.message.answer(
            **BotMessage(
                text=BotStrings.Common.MENU,
                markup=student_main_menu(),
            ).to_aiogram_kwargs()
        )
        await callback.answer()
        return

    data = await state.get_data()
    slot = await services.slot.get_slot(data["reschedule_slot_uuid"])
    request = await services.reschedule.create_request(
        student_uuid=user.uuid,
        slot_uuid=slot.uuid,
        requested_date=data["requested_date"],
        requested_time=data["requested_time"],
    )
    teacher = await services.teacher.get_teacher_by_uuid(request.teacher_uuid)
    old_time = slot.dt_start.strftime(full_format_no_sec)
    new_time = f"{request.requested_date:%d.%m.%Y} {request.requested_time:%H:%M}"
    await sender.send_to_chat(
        chat_id=teacher.chat_id,
        text=BotStrings.Teacher.RESCHEDULE_CREATED.format(
            student=user.username,
            old_time=old_time,
            new_time=new_time,
        ),
    )
    await state.clear()
    await callback.message.answer(
        **BotMessage(
            text=BotStrings.Student.RESCHEDULE_SENT,
            markup=student_main_menu(),
        ).to_aiogram_kwargs()
    )
    await callback.answer()


async def _format_schedule(
    slots: list[SlotDTO], services: Services, user: UserDTO
) -> str:
    lines = [BotStrings.Student.SCHEDULE]
    for slot in slots:
        teacher = await services.teacher.get_teacher_by_uuid(slot.uuid_teacher)
        lesson = await services.lesson.get_student_lesson_for_teacher(
            student_uuid=user.uuid,
            teacher_uuid=slot.uuid_teacher,
        )
        lesson_label = lesson.label if lesson else "-"
        teacher_name = " ".join(
            part for part in [teacher.firstname, teacher.lastname] if part
        )
        lines.append(
            "\n".join(
                [
                    "",
                    slot.dt_start.strftime(full_format_no_sec),
                    f"Преподаватель: {teacher_name or teacher.username}",
                    f"Предмет: {lesson_label}",
                ]
            )
        )
    return "\n".join(lines)


def _parse_date(value: str | None):
    if not value:
        return None
    try:
        return datetime.strptime(value.strip(), day_format).date()
    except ValueError:
        return None


def _parse_time(value: str | None):
    if not value:
        return None
    try:
        return datetime.strptime(value.strip(), time_format_HM).time()
    except ValueError:
        return None
