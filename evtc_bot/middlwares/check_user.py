from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, TelegramObject
from aiogram.utils import markdown

from evtc_bot.db.redis.models import User
from evtc_bot.keyboards.common import CommonButtonsText, build_request_contact_keyboard
from evtc_bot.states.user_states import UserStates


class CheckUserMiddleware(BaseMiddleware):
    """
    Middleware - checking the user for permission to work with the bot
    """

    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        user_id = event.from_user.id

        is_checked_user = await User.is_permission_user(user_id)
        if is_checked_user:
            return await handler(event, data)

        # Get FSM state_key for current user
        state_key: StorageKey = StorageKey(
            chat_id=user_id,
            user_id=user_id,
            bot_id=event.bot.id,
        )
        current_state = await self.storage.get_state(state_key)

        if current_state == UserStates.get_phone:
            return await handler(event, data)

        # Set FSM state for current user to UserStates.get_phone
        await self.storage.set_state(state=UserStates.get_phone, key=state_key)

        text_message = markdown.text(
            f"🤔 {markdown.hbold(event.from_user.full_name)}, сейчас доступ закрыт.",
            "Для начала работы Вам необходимо отправить свой контакт. ",
            f'Нажмите на кнопку "{CommonButtonsText.CONTACT}" 👇',
        )

        if isinstance(event, CallbackQuery):
            await event.answer()
            await event.message.answer(
                text=text_message, reply_markup=build_request_contact_keyboard()
            )
        else:
            await event.answer(
                text=text_message, reply_markup=build_request_contact_keyboard()
            )

        return
