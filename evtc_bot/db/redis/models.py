import json
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ValidationError

from evtc_bot.db.redis.engine import redis


class UserData(BaseModel):
    dt: str
    gn: str
    model: str
    address: str
    article: str
    protocol: str
    parking: str
    photo_protocol: str
    photo_tc: str

    class ConfigDict:
        extra = "allow"


class UserRole(str, Enum):
    """
    Redis model table for user roles
    """

    admin = "admin"
    user = "user"


class User(BaseModel):
    """
    Redis model table for user
    """

    id: int = Field(alias="id")
    name: str = Field(alias="name")
    phone_number: str = Field(alias="phone_number")
    role: UserRole = UserRole.user

    data: Optional[UserData] = None

    class ConfigDict:
        table_name = "users"
        from_attributes = True

    @classmethod
    async def is_permission_user(cls, user_id: int) -> bool:
        # user_data = await redis.get(f"{cls.ConfigDict.table_name}:{user_id}")
        # return True if user_data else None
        user_data = await redis.get(f"{cls.ConfigDict.table_name}:{user_id}")
        if user_data:
            user_data = json.loads(user_data)
            return bool(isinstance(user_data, dict) and user_data.get("phone_number"))
        return False

    @classmethod
    async def get_from_redis(cls, user_id: int):
        user_data = await redis.get(f"{cls.ConfigDict.table_name}:{user_id}")
        if user_data:
            return cls(**json.loads(user_data))
        else:
            return None

    async def save_to_redis(self):
        user_data = json.dumps(self.dict())
        await redis.set(f"{self.ConfigDict.table_name}:{self.id}", user_data)
