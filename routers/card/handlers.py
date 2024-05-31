
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from config import settings
from keyboards.card import build_card_keyboard
from validators.card import validate_gn
from .states import get_card_text, validate_card, CardStates

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


@router.message(CardStates.gn, F.text.cast(validate_gn).as_('gn'))
async def handle_card_gn(message: types.Message, state: FSMContext, gn: str):
    await state.update_data(gn=gn)
    await message.answer(
        text=f'Номер ТС "{markdown.hbold(message.text)}" изменен. 👌',
    )
    await handle_card(message, state)


@router.message(CardStates.gn)
async def handle_card_gn(message: types.Message):
    await message.answer(
        text=markdown.text(
            f'⛔ Ошибочный формат номера ТС - "{markdown.hbold(message.text)}"',
            'Длина номера ТС должна быть в диапазоне 2-9 символов!',
            sep='\n',
        )
    )

#
# @router.message(Survey.full_name)
# async def handle_survey_user_full_name_invalid_content_type(message: types.Message):
#     await message.answer(
#         'Sorry, I didn't understand, send your full name as text.',
#     )
#
#
# @router.message(Survey.email, valid_email_filter)
# async def handle_survey_email_message(
#     message: types.Message,
#     state: FSMContext,
#     email: str,
# ):
#     await state.update_data(email=email)
#     await state.set_state(Survey.email_newsletter)
#     await message.answer(
#         text=(
#             f'Cool, your email is now {markdown.hcode(email)}.'
#             ' Would you like to be contacted in future?'
#         ),
#         reply_markup=build_yes_or_no_keyboard(),
#     )
#
#
# @router.message(Survey.email)
# async def handle_survey_invalid_email_message(message: types.Message):
#     await message.answer(
#         text='Invalid email, please try again.',
#     )
#
#
# async def send_survey_results(message: types.Message, data: dict) -> None:
#     text = markdown.text(
#         'Your survey results:',
#         '',
#         markdown.text('Name:', markdown.hbold(data['full_name'])),
#         markdown.text('Email:', markdown.hcode(data['email'])),
#         (
#             'Cool, we'll send you our news!'
#             if data['newsletter_ok']
#             else 'And we won't bother you again.'
#         ),
#         sep='\n',
#     )
#     await message.answer(
#         text=text,
#         reply_markup=types.ReplyKeyboardRemove(),
#     )
#
#
# @router.message(Survey.email_newsletter, F.text.casefold() == 'yes')
# async def handle_survey_email_newsletter_ok(
#     message: types.Message,
#     state: FSMContext,
# ):
#     data = await state.update_data(newsletter_ok=True)
#     await state.clear()
#     await send_survey_results(message, data)
#
#
# @router.message(Survey.email_newsletter, F.text.casefold() == 'no')
# async def handle_survey_email_newsletter_not_ok(
#     message: types.Message,
#     state: FSMContext,
# ):
#     data = await state.update_data(newsletter_ok=False)
#     await state.clear()
#     await send_survey_results(message, data)
#
#
# @router.message(Survey.email_newsletter)
# async def handle_survey_email_newsletter_could_not_understand(message: types.Message):
#     await message.answer(
#         text=(
#             'Sorry, I didn't understand, '
#             f'please send {markdown.hcode('yes')} or {markdown.hcode('no')}'
#         ),
#         reply_markup=build_yes_or_no_keyboard(),
#     )
