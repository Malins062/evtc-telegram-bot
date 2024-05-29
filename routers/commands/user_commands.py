from aiogram import Router, types
from aiogram.utils import markdown

router = Router(name=__name__)


@router.message()
async def echo_message(message: types.Message):
    await message.reply(
        text=f'🤷‍♂️️ {markdown.hbold(message.from_user.full_name)}, я Вас не понимаю!'
    )
