from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from config import settings, input_data
from keyboards.card import CardButtonText, build_card_keyboard
from routers.card.card_handler import handle_card
from routers.card.states import init_state, get_card_text, validate_card

router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start(message: types.Message, state: FSMContext):
    await message.answer(
        text=markdown.text(
            f'😉 Привет, {markdown.hbold(message.from_user.full_name)}!',
            'Я могу отправить сведения об эвакуации ТС в Управление Госавтоинспекции.',
            ' ',
            'Для отправки сведений, необходимо: ',
            '1) заполнить все данные об эвакуированном ТС;',
            f'2) отправить данные, нажав на кнопку "{CardButtonText.SEND}".',
            sep='\n'
        ),
    )
    user_data = input_data.get(state.key.user_id)
    if not user_data:
        await init_state(state)
    await handle_card(message, state)


@router.message(Command('card', prefix=settings.prefix))
async def handle_init_card(message: types.Message, state: FSMContext):
    await handle_card(message, state)


@router.message(Command('clear', prefix=settings.prefix))
async def handle_clear_card(message: types.Message, state: FSMContext):
    try:
        await init_state(state)
        user_id = state.key.user_id
        user_data = input_data.get(user_id)
        await message.answer(
            text='Карточка очищена 👌',
            show_alert=True,
        )
        await message.answer(
            text=get_card_text(user_data, user_id),
            reply_markup=build_card_keyboard(validate_card(user_data)),
        )
    except Exception as err:
        await message.answer(
            text=f'😢 Ошибка очистки карточки нарушения: {err}',
            cache_time=100,
        )


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
            f'{CardButtonText.SEND} - {markdown.hitalic("отправить заполненные сведения")}',
            sep='\n'
        ),
    )
    await handle_card(message, state)
