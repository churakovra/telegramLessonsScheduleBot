from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.keyboard.callback_factories.notification import (
    NotificationCreateCallback,
    NotificationDeleteCallback,
    NotificationListCallback,
)
from app.keyboard.fabric import (
    cancel_markup,
    notification_buttons,
    teacher_main_menu,
    teacher_sub_menu_notification,
)
from app.message.models import BotMessage
from app.schemas.user import UserDTO
from app.services.container import Services
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import NotificationTriggerType

router = Router()


@router.callback_query(NotificationCreateCallback.filter())
async def create_notification(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(ScheduleStates.wait_for_notification_text)
    await callback.message.answer(
        **BotMessage(
            text=BotStrings.Teacher.NOTIFICATION_ADD_TEXT,
            markup=cancel_markup(),
        ).to_aiogram_kwargs()
    )
    await callback.answer()


@router.callback_query(NotificationListCallback.filter())
async def list_notifications(
    callback: CallbackQuery, services: Services, user: UserDTO
) -> None:
    notifications = await services.notification.get_teacher_notifications(user.uuid)
    if not notifications:
        message = BotMessage(
            text=BotStrings.Teacher.NOTIFICATIONS_NOT_FOUND,
            markup=teacher_sub_menu_notification(),
        )
    else:
        message = BotMessage(
            text=BotStrings.Teacher.NOTIFICATIONS_LIST,
            markup=notification_buttons(notifications=notifications),
        )
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


@router.callback_query(NotificationDeleteCallback.filter(F.confirmed.is_(False)))
async def delete_notification(
    callback: CallbackQuery,
    callback_data: NotificationDeleteCallback,
    services: Services,
) -> None:
    await services.notification.delete_notification(callback_data.uuid)
    await callback.message.answer(
        **BotMessage(
            text=BotStrings.Teacher.NOTIFICATION_DELETE_SUCCESS,
            markup=teacher_sub_menu_notification(),
        ).to_aiogram_kwargs()
    )
    await callback.answer()


@router.message(ScheduleStates.wait_for_notification_text)
async def wait_for_notification_text(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer(
            **BotMessage(text=BotStrings.Errors.INVALID_INPUT).to_aiogram_kwargs()
        )
        return
    await state.update_data(notification_text=message.text.strip())
    await state.set_state(ScheduleStates.wait_for_notification_minutes)
    await message.answer(
        **BotMessage(
            text=BotStrings.Teacher.NOTIFICATION_ADD_MINUTES,
            markup=cancel_markup(),
        ).to_aiogram_kwargs()
    )


@router.message(ScheduleStates.wait_for_notification_minutes)
async def wait_for_notification_minutes(
    message: Message,
    state: FSMContext,
    services: Services,
    user: UserDTO,
) -> None:
    if not message.text:
        await message.answer(
            **BotMessage(text=BotStrings.Errors.INVALID_INPUT).to_aiogram_kwargs()
        )
        return

    try:
        minutes_before = int(message.text.strip())
    except ValueError:
        await message.answer(
            **BotMessage(
                text=BotStrings.Teacher.NOTIFICATION_ADD_MINUTES_ERROR,
                markup=cancel_markup(),
            ).to_aiogram_kwargs()
        )
        return

    data = await state.get_data()
    await services.notification.create_notification(
        teacher_uuid=user.uuid,
        text=data["notification_text"],
        trigger_type=NotificationTriggerType.BEFORE_LESSON,
        minutes_before=minutes_before,
    )
    await state.clear()
    await message.answer(
        **BotMessage(
            text=BotStrings.Teacher.NOTIFICATION_ADD_SUCCESS,
            markup=teacher_main_menu(),
        ).to_aiogram_kwargs()
    )
