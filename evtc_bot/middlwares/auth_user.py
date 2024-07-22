from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import TelegramObject
from aiogram.utils import markdown

from evtc_bot.config.settings import users
from evtc_bot.keyboards.common import CommonButtonsText, build_request_contact_keyboard
from evtc_bot.states.user_states import UserStates


class AuthUserMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage, dispatcher: Dispatcher):
        self.storage = storage
        self.dp = dispatcher

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        if users.get(event.from_user.id):
            return await handler(event, data)

        # Получаем состояние для текущего пользователя
        state: FSMContext = FSMContext(
            storage=self.dp.storage,
            key=StorageKey(
                chat_id=event.chat.id,
                user_id=event.from_user.id,
                bot_id=event.bot.id))
        await state.update_data()  # обновить дату для пользователя

        # Устанавливаем состояние - "Получение контакта"
        await state.set_state(UserStates.get_phone)

        await event.answer(
            text=markdown.text(
                f"🤔 - {markdown.hbold(event.from_user.full_name)}, сейчас доступ закрыт.",
                "Для начала работы Вам необходимо отправить свой контакт. ",
                f'Нажмите на кнопку "{CommonButtonsText.CONTACT}" 👇',
            ),
            reply_markup=build_request_contact_keyboard(),
        )
        return
        # return await handler(event, data)
