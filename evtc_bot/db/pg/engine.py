from sqlalchemy.ext.asyncio import create_async_engine

from evtc_bot.config.settings import settings
from evtc_bot.db.pg.models.base import DeclarativeBase as Base

engine = create_async_engine(settings.db_url, echo=True)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
