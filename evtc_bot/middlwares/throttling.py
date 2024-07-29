import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, Message
from aiogram.utils import markdown

from evtc_bot.config.settings import settings

logger = logging.getLogger(__name__)


class ThrottlingMiddleware(BaseMiddleware):
    """
    Middleware - spam protection
    """

    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:

        user = f"{event.from_user.id}-{event.from_user.full_name}"

        check_user = await self.storage.redis.get(name=user)

        if check_user:
            if int(check_user.decode()) == 1:
                await self.storage.redis.set(
                    name=user, value=0, ex=settings.md.throttle_timeout
                )

                text_message = markdown.hbold(
                    f"ОБНАРУЖЕНА ПОДОЗРИТЕЛЬНАЯ АКТИВНОСТЬ! ПАУЗА - {settings.md.throttle_timeout} СЕКУНД..."
                )
                if isinstance(event, CallbackQuery):
                    await event.answer()
                    await event.message.answer(text_message)
                else:
                    await event.answer(text_message)
                logger.warning(f"Пользователь - {user}. {text_message}")
            return

        await self.storage.redis.set(
            name=user, value=1, px=settings.md.throttle_time_interval
        )

        return await handler(event, data)
