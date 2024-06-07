from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from config_data.config import settings, users
from routers.card.base_handler import handle_card
from states.states import CardStates, set_input_data, Card

router = Router(name=__name__)


@router.message(CardStates.phone_number, F.contact)
async def handle_card_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=True)
    value_phone_number = message.contact.phone_number
    users[state.key.user_id] = value_phone_number
    set_input_data(state, Card(phone_number=value_phone_number))
    await message.answer(
        text=f'✔ Ваш контакт сохранен - {markdown.hbold(value_phone_number)}',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await handle_card(message, state)


@router.message(CardStates.phone_number)
async def handle_card_phone_number(message: types.Message):
    await message.answer(
        text=markdown.text(
            f'⛔ Номер телефона не виден мне в Вашем аккаунте - "{markdown.hbold(message.text)}"',
            'Необходимо разрешить видимость отображения номера телефона.',
            sep='\n',
        )
    )
