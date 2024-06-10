import asyncio

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config_data.config import settings
from loggers.logger import init_logger
from routers import router as main_router


async def main():
    dp = Dispatcher()
    dp.include_router(main_router)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await dp.start_polling(bot)


if __name__ == '__main__':
    init_logger()

    asyncio.run(main())
