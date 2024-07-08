import datetime as dt

from config.settings import settings


def get_now() -> str:
    now = dt.datetime.now()
    return now.strftime(settings.datetime_format)
