from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from evtc_bot.config.values import article
from evtc_bot.db.redis.models import UserData
from evtc_bot.handlers.card.base_handlers import handle_card
from evtc_bot.states.card_states import CardStates, update_user_data

router = Router(name=__name__)


@router.message(CardStates.article, F.text.in_(article))
async def handle_card_article(message: types.Message, state: FSMContext):
    await state.update_data(model=True)
    value_article = article.get(message.text)
    await update_user_data(state.key.user_id, UserData(article=value_article))
    await message.answer(
        text=f"✔ Статья КоАП РФ изменена на - {markdown.hbold(value_article)}",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await handle_card(message, state)


@router.message(CardStates.article)
async def handle_card_invalid_article(message: types.Message):
    await message.reply(
        text=markdown.text(
            "⛔ Ошибочное значение статьи КоАП РФ!",
            "Выберите статью КоАП РФ из предложенного списка 👇",
            sep="\n",
        )
    )
