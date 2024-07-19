import datetime as dt

from bot.config.settings import settings


def get_now() -> str:
    now = dt.datetime.now()
    return now.strftime(settings.dt.format)
