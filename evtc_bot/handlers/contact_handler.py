import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, TelegramObject
from aiogram.utils import markdown

from evtc_bot.filters.is_contact import IsTrueContact
from evtc_bot.handlers.card.base_handlers import handle_card
from evtc_bot.keyboards.common import CommonButtonsText, build_request_contact_keyboard
from evtc_bot.states.card_states import init_state
from evtc_bot.states.user_states import UserStates

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(UserStates.get_phone, F.contact, IsTrueContact())
async def handle_get_true_contact(
    message: types.Message, state: FSMContext, phone_number: str
):
    await state.update_data(get_phone=True)

    await init_state(
        state=state, name=message.from_user.full_name, phone_number=phone_number
    )

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

    # users[user_id] = phone_number
    # await init_state(state)
    #
    logger.info(f"Открыт доступ контакту: #{state.key.user_id} - {phone_number}")

    await message.answer(
        text="✔ Доступ для работы с ботом - открыт.",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await handle_card(message, state)


@router.message(UserStates.get_phone, F.contact)
async def handle_get_fake_contact(message: types.Message):
    logger.warning(
        f"Предоставлен фейковый контакт от: #{message.from_user.id} - {message.from_user.full_name}"
    )
    await message.reply(
        text=markdown.text(
            "⛔ Вы отправили чужой контакт!",
            "Для получения доступа надо быть честным. Отправьте свой контакт! 👇",
            sep="\n",
        )
    )


@router.message(UserStates.get_phone)
async def handle_get_phone_invalid(message: types.Message):
    await message.reply(
        text=markdown.text(
            "⛔ Номер телефона не виден мне в Вашем аккаунте!",
            "Для получения доступа необходимо отправить свой контакт 👇",
            sep="\n",
        )
    )


async def send_contact_request(event: TelegramObject):
    """
    Sending a message requesting to the user to provide their contact
    :param event:
    :return:
    """

    text_message = markdown.text(
        f"🤔 {markdown.hbold(event.from_user.full_name)}, сейчас доступ закрыт.",
        "Для начала работы Вам необходимо отправить свой контакт. ",
        f'Нажмите на кнопку "{CommonButtonsText.CONTACT}" 👇',
    )

    if isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.answer(
            text=text_message, reply_markup=build_request_contact_keyboard()
        )
    else:
        await event.answer(
            text=text_message, reply_markup=build_request_contact_keyboard()
        )

    return
