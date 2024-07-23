from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, TelegramObject
from aiogram.utils import markdown

from evtc_bot.keyboards.common import CommonButtonsText, build_request_contact_keyboard
from evtc_bot.states.user_states import UserStates


class CheckUserMiddleware(BaseMiddleware):
    """
    Middleware - checking the user for permission to work with the bot
    """

    def __init__(self, storage: RedisStorage, dispatcher: Dispatcher):
        self.storage = storage
        self.dp = dispatcher

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        user_id = event.from_user.id

        # Checking the presence of a user in the list of allowed users
        user_exists = await self.storage.redis.sismember("users", str(user_id))

        if user_exists or data.get("phone_number"):
            return await handler(event, data)

        # Get FSM state for current user
        state: FSMContext = FSMContext(
            storage=self.dp.storage,
            key=StorageKey(
                chat_id=user_id,
                user_id=user_id,
                bot_id=event.bot.id,
            ),
        )

        # Set FSM state for current user to UserStates.get_phone
        await state.set_state(UserStates.get_phone)

        text_message = markdown.text(
            f"🤔: {markdown.hbold(event.from_user.full_name)}, сейчас доступ закрыт.",
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
