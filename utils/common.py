import datetime as dt
from pytz import timezone

from config.settings import settings


# def get_now(utc=settings.time_utc) -> str:
def get_now() -> str:
    now = dt.datetime.now(timezone(settings.time_zone))
    # now += dt.timedelta(hours=utc)
    return now.strftime('%d.%m.%Y %H:%M')
