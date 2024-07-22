import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from evtc_bot.config.settings import settings
from evtc_bot.handlers import router as main_router
from evtc_bot.loggers.logger import init_logger
from evtc_bot.middlwares.auth_user import AuthUserMiddleware
from evtc_bot.middlwares.throttling import ThrottlingMiddleware
from evtc_bot.utils.commands import set_user_commands

ALLOWED_UPDATES = ["message", "callback_query", "inline_query"]


async def start_bot(bot: Bot):
    await set_user_commands(bot)
    # await set_admin_commands(evtc_bot)
    await bot.send_message(settings.admin.id, "Бот запущен...")


async def stop_bot(bot: Bot):
    await bot.send_message(settings.admin.id, "Бот остановлен.")


async def start():
    bot = Bot(
        token=str(settings.bot_token),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    storage = RedisStorage.from_url(settings.db.redis_url)
    # storage = RedisStorage.from_url(f"redis://{settings.redis_user}:{settings.redis_pswd}@{settings.redis_host}:22/0")
    dp = Dispatcher(storage=storage)
    dp.include_router(main_router)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.middleware.register(ThrottlingMiddleware(storage))
    dp.message.middleware.register(AuthUserMiddleware(storage, dp))
    dp.callback_query.middleware.register(AuthUserMiddleware(storage, dp))

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    init_logger()

    asyncio.run(start())
