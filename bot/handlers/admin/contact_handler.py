import logging

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from bot.config.settings import users
from bot.filters.is_contact import IsTrueContact
from bot.handlers.card.base_handlers import handle_card
from bot.states.card_states import init_state
from bot.states.user_states import UserStates

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(UserStates.get_phone, F.contact, IsTrueContact())
async def handle_get_true_contact(message: types.Message, state: FSMContext, phone_number: str):
    await state.update_data(get_phone=True)
    user_id = state.key.user_id

    # Access verification
    # if not (phone_number in get_phones()):
    #     logger.warning(f'Отказано в доступе пользователю: #{user_id} - {phone_number}')
    #     await message.reply(
    #         text=markdown.text(
    #             '⛔ Вам запрещен доступ к работе с ботом!',
    #             'Для получения доступа необходимо обратиться к администратору.',
    #             sep='\n',
    #         ),
    #         reply_markup=build_support_keyboard()
    #     )
    #
    #     return

    users[user_id] = phone_number
    await init_state(state)

    logger.info(f'Открыт доступ контакту: #{user_id} - {phone_number}')

    await message.answer(
        text='✔ Доступ для работы с ботом - открыт.',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await handle_card(message, state)


@router.message(UserStates.get_phone, F.contact)
async def handle_get_fake_contact(message: types.Message):
    logger.warning(f'Предоставлен фейковый контакт от: #{message.from_user.id} - {message.from_user.full_name}')
    await message.reply(
        text=markdown.text(
            '⛔ Вы отправили чужой контакт!',
            'Для получения доступа надо быть честным. Отправьте свой контакт! 👇',
            sep='\n',
        )
    )


@router.message(UserStates.get_phone)
async def handle_get_phone_invalid(message: types.Message):
    await message.reply(
        text=markdown.text(
            '⛔ Номер телефона не виден мне в Вашем аккаунте!',
            'Дла получения доступа необходимо отправить свой контакт 👇',
            sep='\n',
        )
    )
