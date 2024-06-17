import asyncio

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config_data.config import settings
from loggers.logger import init_logger
from routers import router as main_router
from utils.commands import set_user_commands, set_admin_commands


async def start_bot(bot: Bot):
    await set_user_commands(bot)
    # await set_admin_commands(bot)
    await bot.send_message(settings.admin_id, 'Бот запущен...')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.admin_id, 'Бот остановлен.')


async def start():
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp.include_router(main_router)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    init_logger()

    asyncio.run(start())
