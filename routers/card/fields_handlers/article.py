from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from config_data.config import settings
from routers.card.base_handler import handle_card
from states.states import CardStates, set_input_data, Card

router = Router(name=__name__)


@router.message(CardStates.article, F.text.in_(settings.select_values['article']))
async def handle_card_article(message: types.Message, state: FSMContext):
    await state.update_data(model=True)
    value_article = settings.select_values['article'].get(message.text)
    set_input_data(state, Card(article=value_article))
    await message.answer(
        text=f'✔ Статья КоАП РФ изменена на - {markdown.hbold(value_article)}',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await handle_card(message, state)


@router.message(CardStates.article)
async def handle_card_invalid_article(message: types.Message):
    await message.answer(
        text=markdown.text(
            f'⛔ Ошибочное значение статьи КоАП РФ - "{markdown.hbold(message.text)}"',
            'Выберите статью КоАП РФ из предложенного списка 👇',
            sep='\n',
        )
    )
