from datetime import datetime, timedelta

from aiogram.filters import BaseFilter
from aiogram.types import Message

from evtc_bot.config.settings import settings
from evtc_bot.utils.common import get_now
from evtc_bot.validators import card


class IsTrueDateTime(BaseFilter):
    async def __call__(self, message: Message):
        user_dt = card.validate_dt(message.text)
        if not user_dt:
            return False

        dt = datetime.strptime(user_dt, settings.dt.format)
        now = datetime.strptime(get_now(), settings.dt.format)
        if (now - timedelta(hours=settings.dt.delta)) <= dt <= now:
            return {"dt": user_dt}
        else:
            return False
