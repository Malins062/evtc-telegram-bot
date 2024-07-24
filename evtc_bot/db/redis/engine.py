from aiogram.fsm.storage.redis import RedisStorage

from evtc_bot.config.settings import settings


CHECKED_USERS = "checked_users"


redis_storage = RedisStorage.from_url(settings.db.redis_url)
# storage = RedisStorage.from_url(f"redis://{settings.redis_user}:{settings.redis_pswd}@{settings.redis_host}:22/0")
