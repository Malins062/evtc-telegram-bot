from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from config import settings
from keyboards.main import build_main_keyboard, MainButtonText

router = Router(name=__name__)


@router.message(CommandStart(), )
async def handle_start(message: types.Message, state: FSMContext):
    await message.answer(
        text=markdown.text(
            f'👮‍♂️ Привет, {markdown.hbold(message.from_user.full_name)}!',
            'Я могу отправить сведения об эвакуации ТС в Управление Госавтоинспекции.',
            ' ',
            f'Для отправки данных, необходимо заполнить данные 👇',
            sep='\n'
        ),
        reply_markup=build_main_keyboard(),
    )


@router.message(Command('help', prefix=settings.prefix))
async def handle_help(message: types.Message):
    await message.answer(
        text=markdown.text(
            f'Чат-бот {markdown.hbold("Эвакуация ТС")}.',
            'Бот предназначен для передачи информации об эвакуированных транспортных средствах.',
            ' ',
            markdown.hbold('Кнопки управления:'),
            f'{MainButtonText.CARD} - {markdown.hitalic("передаваемые сведения о нарушении")}',
            f'{MainButtonText.CLEAR} - {markdown.hitalic("очистить сведения о нарушении")}!r',
            f'{MainButtonText.SEND} - {markdown.hitalic("отправить сведения в УГИБДД")}',
            ' ',
            f'Для отправки данных, необходимо заполнить карточку нарушения, нажав снизу 👇 на клавиатуре',
            markdown.hbold(MainButtonText.CARD),
            sep='\n'
        ),
        reply_markup=build_main_keyboard(),
    )
