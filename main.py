import asyncio
import logging

from aiogram import Dispatcher, Bot, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown

import config

dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer(text=f'Привет, {markdown.hbold(message.from_user.full_name)}!')


@dp.message(Command('help'))
async def handle_help(message: types.Message):
    text = 'Эвакуация ТС. Бот предназначен для передачи информации об эвакуированных транспортных средствах.'
    await message.answer(text=text)


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
