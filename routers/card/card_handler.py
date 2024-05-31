from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config import settings
from keyboards.card import build_card_keyboard
from .states import get_card_text, validate_card

router = Router(name=__name__)


@router.message(Command('card', prefix=settings.prefix))
async def handle_card(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    current_state = await state.get_state()
    if current_state:
        await state.clear()
    await message.answer(
        text=get_card_text(user_data, state.key.user_id),
        reply_markup=build_card_keyboard(validate_card(user_data)),
    )
