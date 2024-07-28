from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from evtc_bot import __version__
from evtc_bot.config.settings import settings
from evtc_bot.handlers.card.base_handlers import handle_card
from evtc_bot.keyboards.card import (
    CARD_BUTTONS,
    SEND_BUTTON,
    get_annotations_card_buttons,
)
from evtc_bot.states.card_states import init_state

router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start(message: types.Message, state: FSMContext):
    await message.answer(
        text=markdown.text(
            f"😉 Привет, {markdown.hbold(message.from_user.full_name)}!",
            "Я могу отправить сведения об эвакуированном транспортном средстве, туда куда надо!",
            " ",
            "Для отправки сведений, необходимо: ",
            "1) отправить свой контакт (если вы впервые начали работать с ботом);",
            "2) заполнить все данные об эвакуированном ТС;",
            f'3) отправить данные, нажав на кнопку "{CARD_BUTTONS[SEND_BUTTON].title}".',
            sep="\n",
        ),
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await handle_card(message, state)


@router.message(Command("card", prefix=settings.prefixes_command))
async def handle_init_card(message: types.Message, state: FSMContext):
    await handle_card(message, state)


@router.message(Command("clear", prefix=settings.prefixes_command))
async def handle_clear_card(message: types.Message, state: FSMContext):
    await init_state(state)
    await message.answer(
        text="Карточка очищена 👌",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await handle_card(message, state)


@router.message(Command("help", prefix=settings.prefixes_command))
async def handle_help(message: types.Message, state: FSMContext):
    await message.answer(
        text=markdown.text(
            f'Чат-бот {markdown.hbold("Эвакуация ТС")} (v{markdown.hitalic(__version__)}).',
            "Бот предназначен для передачи информации об эвакуированных транспортных средствах.",
            " ",
            markdown.hbold("Кнопки управления:"),
            get_annotations_card_buttons(),
            sep="\n",
        ),
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await handle_card(message, state)
