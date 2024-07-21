import logging

from aiogram import F, Router, types
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

from evtc_bot.config.settings import input_data
from evtc_bot.config.values import article, gn, model, parking
from evtc_bot.handlers.card.base_handlers import handle_card
from evtc_bot.keyboards.card import (
    CardActions,
    CardCbData,
)
from evtc_bot.keyboards.common import build_values_keyboard
from evtc_bot.states.card_states import CardStates, init_state
from evtc_bot.utils.common import get_now
from evtc_bot.utils.smtp import send_data

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.callback_query(CardCbData.filter(F.action == CardActions.dt))
async def card_dt_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.dt)
    await callback_query.answer()
    await callback_query.message.answer(
        text="📅 Введите дату и время задержания ТС:",
        reply_markup=build_values_keyboard(tuple([get_now()])),
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.gn))
async def card_gn_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.gn)
    await callback_query.answer()
    await callback_query.message.answer(
        text="🚘 Введите номер ТС:",
        reply_markup=build_values_keyboard(gn),
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.model))
async def card_model_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.model)
    await callback_query.answer()
    await callback_query.message.answer(
        text="🚗 Введите модель ТС:",
        reply_markup=build_values_keyboard(model),
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.article))
async def card_article_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.article)
    await callback_query.answer()
    await callback_query.message.answer(
        text="👩‍⚖️ Выберите статью КоАП РФ 👇",
        reply_markup=build_values_keyboard(article, sizes=2),
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.parking))
async def card_parking_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.parking)
    await callback_query.answer()
    await callback_query.message.answer(
        text="🏁️ Выберите место стоянки, задержанного ТС 👇",
        reply_markup=build_values_keyboard(parking, sizes=2),
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.protocol))
async def card_protocol_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.protocol)
    await callback_query.answer()
    await callback_query.message.answer(
        text="📃 Введите номер протокола задержания ТС:",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.address))
async def card_address_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.address)
    await callback_query.answer()
    await callback_query.message.answer(
        text="🌍 Введите место нарушения ТС (улица, дом):",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.photo_protocol))
async def card_photo_protocol_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.photo_protocol)
    await callback_query.answer()
    await callback_query.message.answer(
        text="📷 Приложите фото протокола задержания, нажмите - 📎",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.photo_tc))
async def card_photo_tc_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.photo_tc)
    await callback_query.answer()
    await callback_query.message.answer(
        text="📷 Приложите фото нарушения ТС, нажмите - 📎",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.send))
async def card_send_cb(callback_query: CallbackQuery, state: FSMContext):
    try:
        await callback_query.message.bot.send_chat_action(
            chat_id=callback_query.message.chat.id,
            action=ChatAction.UPLOAD_DOCUMENT,
        )

        user_id = state.key.user_id
        user_data = input_data.get(user_id)
        message_subject = (
            f'{user_data.get("gn")} - {user_data.get("model")}: {user_data.get("address")} '
            f'({user_data.get("phone_number")}) #{state.key.bot_id}'
        )

        async with ChatActionSender.upload_document(
            bot=callback_query.message.bot,
            chat_id=callback_query.message.chat.id,
        ):
            # Send email
            await send_data(message_subject, user_data)

        message_text = "Сведения о нарушении успешно отправлены"
        logger.info(f"{message_text}: {user_data}")

        message_text += " 👌"
        await callback_query.answer(message_text)
        await callback_query.message.answer(message_text)

        await init_state(state)
        await handle_card(callback_query.message, state)

    except Exception as err:
        error_text = "Ошибка при отправке карточки"
        logger.error(f"{error_text}: {err}")

        error_text += " 🥵"
        await callback_query.answer(error_text)
        await callback_query.message.answer(error_text)
