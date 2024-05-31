from datetime import datetime


def get_now() -> str:
    return datetime.now().strftime('%d.%m.%Y %H:%M')
