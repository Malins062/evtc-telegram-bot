import asyncio
import logging

from aiogram import Dispatcher, Bot, types
from aiogram.enums import ParseMode

import config
from routers import router as main_router

dp = Dispatcher()

dp.include_router(main_router)


@dp.message()
async def echo_message(message: types.Message):

    await message.answer(
        text='Wait a second...',
    )
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Something new 🙂')


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=config.BOT_TOKEN,
        parse_mode=ParseMode.HTML,
    )
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
