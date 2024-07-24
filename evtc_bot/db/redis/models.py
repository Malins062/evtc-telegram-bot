from enum import Enum

from pydantic import BaseModel

from evtc_bot.db.redis.engine import redis_storage


class UserRole(str, Enum):
    admin = "admin"
    user = "user"


class User(BaseModel):
    id: int
    username: str
    role: UserRole

    @classmethod
    async def get_from_redis(cls, user_id: int):
        user_data = await redis_storage.get(f"user:{user_id}")
        if user_data:
            return cls(**user_data)
        else:
            return None

    async def save_to_redis(self):
        await redis_storage.set(f"user:{self.id}", self.dict())
