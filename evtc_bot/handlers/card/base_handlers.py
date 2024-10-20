from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from evtc_bot.db.redis.models import User
from evtc_bot.keyboards.card import build_card_keyboard
from evtc_bot.keyboards.common import CommonButtonsText, build_request_contact_keyboard
from evtc_bot.states.card_states import (
    get_card_text,
    reset_state,
    validate_card,
)
from evtc_bot.states.user_states import UserStates


async def handle_card(message: types.Message, state: FSMContext):
    user_id = state.key.user_id
    user = await User.get_from_redis(user_id)
    # data = {'id': 200287812, 'name': 'Алексей', 'phone': '+79206328673', 'role': 'user'}
    # user = User(**data)
    # user_data = input_data.get(user_id)
    # if not user_data:
    #     await init_state(state)
    #     user_data = input_data.get(user_id)

    await reset_state(state)
    await message.answer(
        text=get_card_text(user),
        reply_markup=build_card_keyboard(validate_card(user.data)),
    )

    # if users.get(user_id):
    #     await reset_state(state)
    #     await message.answer(
    #         text=get_card_text(user_data),
    #         reply_markup=build_card_keyboard(validate_card(user_data)),
    #     )
    # else:
    #     await handle_contact(message, state)
    #


async def handle_contact(message: types.Message, state: FSMContext):
    await state.set_state(UserStates.get_phone)
    await message.answer(
        text=markdown.text(
            f"🤔 - {markdown.hbold(message.from_user.full_name)}, сейчас доступ закрыт.",
            "Для начала работы Вам необходимо отправить свой контакт. ",
            f'Нажмите на кнопку "{CommonButtonsText.CONTACT}" 👇',
        ),
        reply_markup=build_request_contact_keyboard(),
    )
