from datetime import datetime, timedelta

from aiogram.filters import BaseFilter
from aiogram.types import Message
from pydantic import ValidationError

import validators.card
from config.settings import settings
from utils.common import get_now


class IsTrueDateTime(BaseFilter):
    async def __call__(self, message: Message):
        user_dt = validators.card.validate_dt(message.text)
        if not user_dt:
            return False

        dt = datetime.strptime(user_dt, settings.datetime_format)
        now = datetime.strptime(get_now(), settings.datetime_format)
        if (now - timedelta(hours=settings.datetime_delta)) <= dt <= now:
            return {'dt': user_dt}
        else:
            return False
