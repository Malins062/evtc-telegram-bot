import asyncio

from aiogram import Dispatcher, Bot, types

BOT_TOKEN = '7005910963:AAGPlaw25ivbytySZWlHX7v9F7Hqn5QtXQo'

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
