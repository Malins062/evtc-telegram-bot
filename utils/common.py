import datetime as dt

from config_data.config import settings


def get_now(utc=settings.time_utc) -> str:
    now = dt.datetime.now()
    now += dt.timedelta(hours=utc)
    return now.strftime('%d.%m.%Y %H:%M')
