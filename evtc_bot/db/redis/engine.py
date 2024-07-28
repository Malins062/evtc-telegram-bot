from aiogram.fsm.storage.redis import RedisStorage

from evtc_bot.config.settings import settings

# from evtc_bot.db.redis.models import User

# Redis storage
redis_storage = RedisStorage.from_url(settings.db.redis_url)
# storage = RedisStorage.from_url(f"redis://{settings.redis_user}:{settings.redis_pswd}@{settings.redis_host}:22/0")

# Redis
redis = redis_storage.redis


# def get_user(user_id):
#     user_data = r.hgetall(f'{User.__name__}:{user_id}')
#     if user_data:
#         return User(user_data[b'id'], user_data[b'username'])
#     return None
#
#
# def save_user(user):
#     r.hmset(f'{User.__name__}:{user.id}', {'id': user.id, 'username': user.username})
#
