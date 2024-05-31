from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from keyboards.card import (
    CardCbData,
    CardActions, 
    build_card_keyboard,
)
from routers.card.states import init_state, get_card_text

router = Router(name=__name__)


@router.callback_query(
    CardCbData.filter(F.action == CardActions.clear),
)
async def card_clear_cb(callback_query: CallbackQuery, state: FSMContext):
    try:
        await init_state(state)
        user_data = await state.get_data()
        # print(user_data)
        await callback_query.answer(
            text='Карточка очищена 👌',
            cache_time=100,
        )
        await callback_query.message.edit_text(
            text=get_card_text(user_data, state.key.user_id),
            reply_markup=build_card_keyboard(),
        )
    except Exception as err:
        await callback_query.answer(
            text=f'😢 Ошибка очистки карточки нарушения: {err}',
            cache_time=100,
        )
