from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from validators.card import validate_model
from .card_handler import handle_card
from .states import CardStates, set_input_data, Card

router = Router(name=__name__)


@router.message(CardStates.article, F.text.cast(validate_model).as_('article'))
async def handle_card_article(message: types.Message, state: FSMContext, article: str):
    await state.update_data(model=True)
    set_input_data(state, Card(article=article))
    await message.answer(
        text=f'✔ Статья КоАП РФ изменена на - {markdown.hbold(article)}',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await handle_card(message, state)


@router.message(CardStates.article)
async def handle_card_invalid_article(message: types.Message):
    await message.answer(
        text=markdown.text(
            f'⛔ Ошибочный статьи КоАП РФ - "{markdown.hbold(message.text)}"',
            'Длина строки статьи КоАП РФ должна быть в диапазоне 2-300 символов!',
            sep='\n',
        )
    )
