import datetime as dt
from pytz import timezone

from evtc_bot.config.settings import settings


def get_now() -> str:
    now = dt.datetime.now(timezone(settings.time_zone))
    return now.strftime(settings.datetime_format)
