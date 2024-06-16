from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from config_data.config import settings, users
from keyboards.card import CARD_BUTTONS, SEND_BUTTON, get_annotations_card_buttons
from routers.card.base_handlers import handle_card
from states.card_states import init_state

router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start(message: types.Message, state: FSMContext):
    await message.answer(
        text=markdown.text(
            f'😉 Привет, {markdown.hbold(message.from_user.full_name)}!',
            'Я могу отправить сведения об эвакуированном транспортном средстве, туда куда надо!',
            ' ',
            'Для отправки сведений, необходимо: ',
            '1) отправить свой контакт (если вы впервые начали работать с ботом);',
            '2) заполнить все данные об эвакуированном ТС;',
            f'3) отправить данные, нажав на кнопку "{CARD_BUTTONS[SEND_BUTTON].title}".',
            sep='\n',
        ),
    )
    await handle_card(message, state)


@router.message(Command('card', prefix=settings.prefix))
async def handle_init_card(message: types.Message, state: FSMContext):
    await handle_card(message, state)


@router.message(Command('clear', prefix=settings.prefix))
async def handle_clear_card(message: types.Message, state: FSMContext):
    await init_state(state)

    user_id = state.key.user_id
    if users.get(user_id):
        try:
            await message.answer(
                text='Карточка очищена 👌',
                show_alert=True,
            )
            # await message.answer(
            #     text=get_card_text(user_data),
            #     reply_markup=build_card_keyboard(validate_card(user_data)),
            # )
        except Exception as err:
            await message.answer(
                text=f'😢 Ошибка очистки карточки нарушения: {err}',
                cache_time=100,
            )
    await handle_card(message, state)


@router.message(Command('help', prefix=settings.prefix))
async def handle_help(message: types.Message, state: FSMContext):
    await message.answer(
        text=markdown.text(
            f'Чат-бот {markdown.hbold("Эвакуация ТС")}.',
            'Бот предназначен для передачи информации об эвакуированных транспортных средствах.',
            ' ',
            markdown.hbold('Кнопки управления:'),
            get_annotations_card_buttons(),
            sep='\n'
        ),
    )
    await handle_card(message, state)
