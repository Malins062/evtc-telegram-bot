from aiogram.filters import Filter
from aiogram.types import Message

from bot.config.settings import input_data, settings


class IsAdminUser(Filter):
    _NAME_FIELD = "phone_number"

    def __init__(self) -> None:
        self.phone_numbers = settings.admin.phone_numbers

    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        data = input_data.get(user_id)
        if not (data and (self._NAME_FIELD in data)):
            return False
        return data.get(self._NAME_FIELD) in self.phone_numbers
