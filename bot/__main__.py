import asyncio

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from bot.config.settings import settings
from bot.loggers.logger import init_logger
from bot.handlers import router as main_router
from bot.utils.commands import set_user_commands
from bot.middlwares.throttling import ThrottlingMiddleware


ALLOWED_UPDATES = ["message", "callback_query", "inline_query"]


async def start_bot(bot: Bot):
    await set_user_commands(bot)
    # await set_admin_commands(bot)
    await bot.send_message(settings.admin_id, "Бот запущен...")


async def stop_bot(bot: Bot):
    await bot.send_message(settings.admin_id, "Бот остановлен.")


async def start():
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    storage = RedisStorage.from_url(settings.db.redis_url)
    # storage = RedisStorage.from_url(f"redis://{settings.redis_user}:{settings.redis_pswd}@{settings.redis_host}:22/0")
    dp = Dispatcher(storage=storage)
    dp.include_router(main_router)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.middleware.register(ThrottlingMiddleware(storage))

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    init_logger()

    asyncio.run(start())
