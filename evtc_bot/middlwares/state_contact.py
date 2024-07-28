from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import TelegramObject

from evtc_bot.handlers.contact_handler import send_contact_request
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
            # Send a message requesting to current user to provide their contact
            await send_contact_request(event)

            return None

        return await handler(event, data)
