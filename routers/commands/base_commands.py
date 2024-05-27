from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown

router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer(text=f'Привет, {markdown.hbold(message.from_user.full_name)}!')


@router.message(Command('help', prefix='!?%-'))
async def handle_help(message: types.Message):
    text = 'Эвакуация ТС. Бот предназначен для передачи информации об эвакуированных транспортных средствах.'
    await message.answer(text=text)
