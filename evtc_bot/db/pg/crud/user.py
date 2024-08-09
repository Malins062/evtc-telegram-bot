from evtc_bot.db.pg.models.user import User
from evtc_bot.db.redis.models import User as UserSchema


async def create_users_table(engine):
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)


async def add_user(engine, user: UserSchema):
    async with engine.acquire() as conn:
        await conn.execute(User.__table__.insert().values(user.dict(by_alias=True)))


async def get_user_by_id(engine, user_id: int):
    async with engine.acquire() as conn:
        result = await conn.execute(User.__table__.select().where(User.user_id == user_id))
        return await result.first()


async def update_username(engine, user: UserSchema):
    async with engine.acquire() as conn:
        await conn.execute(User.__table__.update().
                           where(User.user_id == user.user_id).
                           values(user.dict(exclude=user.user_id, by_alias=True)))


async def delete_user(engine, user_id: int):
    async with engine.begin() as conn:
        await conn.execute(User.__table__.delete().where(User.user_id == user_id))
