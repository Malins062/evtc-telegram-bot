import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config_data.config import settings
from routers import router as main_router


async def main():
    dp = Dispatcher()
    dp.include_router(main_router)

    file_log = logging.FileHandler(filename=settings.log_file, mode='w')
    console_out = logging.StreamHandler()
    format_log = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    # logging.basicConfig(handlers=(file_log, console_out),
    logging.basicConfig(handlers=(console_out,),
                        level=logging.INFO,
                        format=format_log)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
