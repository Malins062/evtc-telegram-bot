from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import TelegramObject

from evtc_bot.db.redis.models import User
from evtc_bot.handlers.contact_handler import send_contact_request
from evtc_bot.middlwares.common import get_current_state
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

        # Get current state for current user
        current_state, state_key = await get_current_state(
            self.storage, user_id, event.bot.id
        )
        if current_state == UserStates.get_phone:
            return await handler(event, data)

        # Set FSM state for current user to UserStates.get_phone
        await self.storage.set_state(state=UserStates.get_phone, key=state_key)

        # Send a message requesting to current user to provide their contact
        await send_contact_request(event)

        return
