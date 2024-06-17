from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from config.admin import get_phones
from config.settings import settings
from filters.is_admin import IsAdminUser
from keyboards.common import build_values_keyboard
from states.card_states import reset_state
from states.user_states import UserStates

router = Router(name=__name__)


@router.message(Command('add_user', prefix=settings.prefix), IsAdminUser())
async def handle_add_user(message: types.Message, state: FSMContext):
    await state.set_state(UserStates.add_phone)
    await message.answer(
        text='☎ Введите номер номер телефона пользователя для добавления в список разрешенных:',
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.message(Command('remove_user', prefix=settings.prefix), IsAdminUser())
async def handle_remove_user(message: types.Message, state: FSMContext):
    await state.set_state(UserStates.remove_phone)
    phones_list = get_phones(is_all=False)
    await message.answer(
        text='📵 Введите номер номер телефона пользователя для удаления из список разрешенных:',
        reply_markup=build_values_keyboard(phones_list),
    )


@router.message(Command('list_users', prefix=settings.prefix), IsAdminUser())
async def handle_list_users(message: types.Message, state: FSMContext):
    await reset_state(state)
    phone_numbers = get_phones(is_all=False)
    text_msg = markdown.hbold('Вот список телефонов для разрешенных пользователей:')
    for ind, value in enumerate(phone_numbers):
        text_msg += f'\n{ind+1}) {value}'

    await message.answer(
        text=text_msg,
        reply_markup=types.ReplyKeyboardRemove(),
    )
