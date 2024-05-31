from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import settings
from keyboards.card import (
    CardCbData,
    CardActions, 
    build_card_keyboard,
)
from keyboards.common import build_values_keyboard
from routers.card.states import init_state, get_card_text, validate_card, CardStates
from utils.common import get_now

router = Router(name=__name__)


@router.callback_query(CardCbData.filter(F.action == CardActions.dt))
async def card_gn_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.dt)
    await callback_query.answer()
    await callback_query.message.answer(
        text='📅 Введите дату и время задержания ТС:',
        reply_markup=build_values_keyboard([get_now()])
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.gn))
async def card_gn_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.gn)
    await callback_query.answer()
    await callback_query.message.answer(
        text='🚘 Введите номер ТС:',
        reply_markup=build_values_keyboard(settings.select_values['gn'])
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.model))
async def card_model_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.model)
    await callback_query.answer()
    await callback_query.message.answer(
        text='🚗 Введите модель ТС:',
        reply_markup=build_values_keyboard(settings.select_values['model'])
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.clear))
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
            reply_markup=build_card_keyboard(validate_card(user_data)),
        )
    except Exception as err:
        await callback_query.answer(
            text=f'😢 Ошибка очистки карточки нарушения: {err}',
            cache_time=100,
        )
