import json
from enum import Enum
from typing import Optional, TypeVar

from pydantic import BaseModel, Field

from evtc_bot.db.redis.engine import redis

StrType = TypeVar("StrType", str, None)


class Data(BaseModel):
    """
    Redis model for data card violation
    """

    dt: Optional[StrType] = Field(default=None)
    gn: Optional[StrType] = Field(default=None)
    model: Optional[StrType] = Field(default=None)
    address: Optional[StrType] = Field(default=None)
    article: Optional[StrType] = Field(default=None)
    protocol: Optional[StrType] = Field(default=None)
    parking: Optional[StrType] = Field(default=None)
    photo_protocol: Optional[StrType] = Field(default=None)
    photo_tc: Optional[StrType] = Field(default=None)

    class ConfigDict:
        extra = "allow"


class Role(str, Enum):
    """
    Redis model table for user roles
    """

    admin = "admin"
    user = "user"
    inspector = "inspector"


class User(BaseModel):
    """
    Redis model table for user
    """

    id: int = Field(alias="id")
    name: StrType = Field(alias="name")
    full_name: StrType = Field(alias="full_name")
    phone_number: str = Field(alias="phone_number")
    role: Role = Role.user
    access: bool = False

    data: Optional[Data] = None

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
