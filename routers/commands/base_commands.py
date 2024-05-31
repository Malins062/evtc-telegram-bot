from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from config import settings
from keyboards.card import CardButtonText
from routers.card.handlers import handle_card
from routers.card.states import init_state

router = Router(name=__name__)


@router.message(CommandStart(), )
async def handle_start(message: types.Message, state: FSMContext):
    await message.answer(
        text=markdown.text(
            f'👮‍♂️ Привет, {markdown.hbold(message.from_user.full_name)}!',
            'Я могу отправить сведения об эвакуации ТС в Управление Госавтоинспекции.',
            ' ',
            'Для отправки сведений, необходимо: ',
            '1) заполнить все данные об эвакуированном ТС;',
            f'2) отправить данные, нажав на кнопку "{CardButtonText.SEND}".',
            sep='\n'
        ),
    )
    await init_state(state)
    await handle_card(message, state)


@router.message(Command('help', prefix=settings.prefix))
async def handle_help(message: types.Message, state: FSMContext):
    await message.answer(
        text=markdown.text(
            f'Чат-бот {markdown.hbold("Эвакуация ТС")}.',
            'Бот предназначен для передачи информации об эвакуированных транспортных средствах в Управление '
            'Госавтоинспекции.',
            ' ',
            markdown.hbold('Кнопки управления:'),
            f'{CardButtonText.DT} - {markdown.hitalic("указать дату и время нарушения")}',
            f'{CardButtonText.ADDRESS} - {markdown.hitalic("указать адрес правонарушения")}',
            f'{CardButtonText.GN} - {markdown.hitalic("изменить гос.номер, задерживаемого ТС")}',
            f'{CardButtonText.MODEL} - {markdown.hitalic("изменить модель ТС")}',
            f'{CardButtonText.ARTICLE} - {markdown.hitalic("указать статью КоАП РФ")}',
            f'{CardButtonText.PROTOCOL} - {markdown.hitalic("изменить номер протокола задержания ТС")}',
            f'{CardButtonText.CLEAR} - {markdown.hitalic("очистить все сведения о нарушении")}',
            f'{CardButtonText.SEND} - {markdown.hitalic("отправить заполненные сведения")}',
            sep='\n'
        ),
    )
    await handle_card(message, state)
