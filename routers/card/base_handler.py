from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from config_data.config import input_data, users
from keyboards.card import build_card_keyboard
from keyboards.common import build_request_contact_keyboard, CommonButtonsText
from states.states import get_card_text, validate_card, reset_state, init_state, CardStates


async def handle_card(message: types.Message, state: FSMContext):
    user_id = state.key.user_id
    user_data = input_data.get(user_id)
    if not user_data:
        await init_state(state)
        user_data = input_data.get(user_id)

    if users.get(user_id):
        await reset_state(state)
        await message.answer(
            text=get_card_text(user_data),
            reply_markup=build_card_keyboard(validate_card(user_data)),
        )
    else:
        await handle_contact(message, state)


async def handle_contact(message: types.Message, state: FSMContext):
    await state.set_state(CardStates.phone_number)
    await message.answer(
        text=markdown.text(
            f'🤔 - {markdown.hbold(message.from_user.full_name)}, ',
            'для начала работы, необходимо отправить свой контакт. ',
            f'Нажмите на кнопку "{CommonButtonsText.CONTACT}" 👇',
        ),
        reply_markup=build_request_contact_keyboard(),
    )


