import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from evtc_bot import __version__
from evtc_bot.config.settings import settings
from evtc_bot.db.redis import redis_storage as storage
from evtc_bot.handlers import router as main_router
from evtc_bot.loggers.logger import init_logger
from evtc_bot.middlwares.check_user import CheckUserMiddleware
from evtc_bot.middlwares.throttling import ThrottlingMiddleware
from evtc_bot.utils.commands import set_user_commands

ALLOWED_UPDATES = ["message", "callback_query", "inline_query"]


async def start_bot(bot: Bot):
    await set_user_commands(bot)
    # await set_admin_commands(evtc_bot)
    await bot.send_message(settings.admin.id, f"Бот (версия {__version__}) запущен...")


async def stop_bot(bot: Bot):
    await bot.send_message(settings.admin.id, f"Бот (версия {__version__}) остановлен.")


async def start():
    bot = Bot(
        token=str(settings.bot_token),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher(storage=storage)
    dp.include_router(main_router)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # Spam protection
    dp.message.middleware.register(ThrottlingMiddleware(storage))

    # Checking the user for permission to work with the bot
    dp.message.middleware.register(CheckUserMiddleware(storage, dp))
    dp.callback_query.middleware.register(CheckUserMiddleware(storage, dp))

    try:
        # Ignoring all cached commands before the bot starts working
        await bot.delete_webhook(drop_pending_updates=True)

        # Start polling with only ALLOWED updates
        await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    init_logger()

    asyncio.run(start())
