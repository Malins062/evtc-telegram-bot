from aiogram import types
from aiogram.fsm.context import FSMContext

from config_data.config import input_data
from keyboards.card import build_card_keyboard
from states.states import get_card_text, validate_card, reset_state


async def handle_card(message: types.Message, state: FSMContext):
    user_id = state.key.user_id
    user_data = input_data.get(user_id)
    await reset_state(state)
    await message.answer(
        text=get_card_text(user_data, user_id),
        reply_markup=build_card_keyboard(validate_card(user_data)),
    )
