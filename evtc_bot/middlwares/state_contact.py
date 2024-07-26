from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, TelegramObject
from aiogram.utils import markdown

from evtc_bot.db.redis.models import User
from evtc_bot.keyboards.common import CommonButtonsText, build_request_contact_keyboard
from evtc_bot.states.user_states import UserStates


class CheckContactStateMiddleware(BaseMiddleware):
    """
    Middleware for check active state for get user contact
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

        # Get FSM state_key for current user
        state_key: StorageKey = StorageKey(
            chat_id=user_id,
            user_id=user_id,
            bot_id=event.bot.id,
        )
        current_state = await self.storage.get_state(state_key)

        if current_state == UserStates.get_phone:
            return

        return await handler(event, data)

    # async def __call__(self, update, next_handler):
    #     state: FSMContext = update.get_current_state()
    #     current_state = await state.get_state()
    #
    #     if current_state == UserStates.get_phone:
    #         return
    #
    #     return await next_handler(update)
