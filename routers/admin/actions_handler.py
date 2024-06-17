import logging

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from config_data.admin import add_phone, get_phones, save_phones
from filters.is_admin import IsAdminUser
from states.user_states import UserStates
from validators.admin import validate_phone_number
from routers.card.base_handlers import handle_card

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(UserStates.add_phone,
                F.text.cast(validate_phone_number).as_('phone_number'),
                IsAdminUser())
async def handle_add_phone_number(message: types.Message, state: FSMContext, phone_number: str):
    await state.update_data(add_phone=True)

    phone_list = get_phones(is_all=False)
    if phone_number in phone_list:
        await message.reply(
            text=f'😯 Номер телефона уже есть в списке разрешенных.',
            reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        if add_phone(phone_number):
            text_msg = 'Указанный номер телефона успешно внесен в список разрешенных.'
            logger.info(text_msg)
        else:
            text_msg = 'К сожалению, номер указанный телефона не добавлен список разрешенных.'
            logger.warning(text_msg)

        await message.reply(
            text=text_msg,
            reply_markup=types.ReplyKeyboardRemove()
        )

    await handle_card(message, state)


@router.message(UserStates.remove_phone,
                F.text,
                IsAdminUser())
async def handle_remove_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(remove_phone=True)

    phone_list = get_phones(is_all=False)
    if not (F.text in phone_list):
        await message.reply(
            text='😯 Указанный номер телефона не найден в списке разрешенных.',
            reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        phone_list = list(phone_list)
        phone_list.remove(F.text)

        if save_phones(phone_list):
            text_msg = 'Указанный номер телефона успешно удален из списка разрешенных.'
            logger.info(text_msg)
        else:
            text_msg = 'К сожалению, указанный номер телефона не удален из списка разрешенных.'
            logger.warning(text_msg)

        await message.reply(
            text=text_msg,
            reply_markup=types.ReplyKeyboardRemove()
        )

    await handle_card(message, state)


@router.message(UserStates.add_phone)
async def handle_invalid_phone_number(message: types.Message):
    await message.reply(
        text=markdown.text(
            '⛔ Ошибочный номера телефона!',
            'Формат значения: +NNNNNNNNNNN, N - цифра (от 7 до 15 цифр).',
            sep='\n',
        )
    )
