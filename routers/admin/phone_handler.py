import logging

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from config_data.config import users
from config_data.admin import get_phones
from keyboards.common import build_support_keyboard
from routers.card.base_handlers import handle_card
from states.card_states import init_state
from states.user_states import UserStates

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(UserStates.get_phone, F.contact)
async def handle_get_phone(message: types.Message, state: FSMContext):
    await state.update_data(get_phone=True)
    value_phone_number = message.contact.phone_number
    user_id = state.key.user_id

    # Access verification
    if not (value_phone_number in get_phones()):
        logger.warning(f'Отказано в доступе пользователю: #{user_id} - {value_phone_number}')
        await message.reply(
            text=markdown.text(
                '⛔ Вам запрещен доступ к работе с ботом!',
                'Для получения доступа необходимо обратиться к администратору.',
                sep='\n',
            ),
            reply_markup=build_support_keyboard()
        )

        return

    users[user_id] = value_phone_number
    await init_state(state)

    logger.info(f'Открыт доступ контакту: #{state.key.user_id} - {value_phone_number}')

    await message.answer(
        text='✔ Доступ для работы с ботом - открыт.',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await handle_card(message, state)


@router.message(UserStates.get_phone)
async def handle_get_phone_invalid(message: types.Message):
    await message.reply(
        text=markdown.text(
            '⛔ Номер телефона не виден мне в Вашем аккаунте!',
            'Необходимо разрешить видимость отображения номера телефона.',
            sep='\n',
        ),
        reply_markup=build_support_keyboard()
    )
