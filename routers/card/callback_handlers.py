import logging

from aiogram import Router, F, types
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

from config.settings import settings, input_data
from keyboards.card import (
    CardCbData,
    CardActions,
)
from keyboards.common import build_values_keyboard
from routers.card.base_handlers import handle_card
from states.card_states import init_state, CardStates
from utils.common import get_now
from utils.smtp import send_data

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.callback_query(CardCbData.filter(F.action == CardActions.dt))
async def card_gn_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.dt)
    await callback_query.answer()
    await callback_query.message.answer(
        text='📅 Введите дату и время задержания ТС:',
        reply_markup=build_values_keyboard([get_now()])
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.gn))
async def card_gn_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.gn)
    await callback_query.answer()
    await callback_query.message.answer(
        text='🚘 Введите номер ТС:',
        reply_markup=build_values_keyboard(settings.select_values['gn'])
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.model))
async def card_model_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.model)
    await callback_query.answer()
    await callback_query.message.answer(
        text='🚗 Введите модель ТС:',
        reply_markup=build_values_keyboard(settings.select_values['model'])
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.article))
async def card_article_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.article)
    await callback_query.answer()
    await callback_query.message.answer(
        text='👩‍⚖️ Выберите статью КоАП РФ 👇',
        reply_markup=build_values_keyboard(settings.select_values['article'], sizes=2)
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.parking))
async def card_parking_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.parking)
    await callback_query.answer()
    await callback_query.message.answer(
        text='🏁️ Выберите место стоянки, задержанного ТС 👇',
        reply_markup=build_values_keyboard(settings.select_values['parking'], sizes=2)
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.protocol))
async def card_protocol_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.protocol)
    await callback_query.answer()
    await callback_query.message.answer(
        text='📃 Введите номер протокола задержания ТС:',
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.address))
async def card_address_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.address)
    await callback_query.answer()
    await callback_query.message.answer(
        text='🌍 Введите место нарушения ТС (улица, дом):',
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.photo_protocol))
async def card_photo_protocol_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.photo_protocol)
    await callback_query.answer()
    await callback_query.message.answer(
        text='📷 Приложите фото протокола задержания, нажмите - 📎',
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.callback_query(CardCbData.filter(F.action == CardActions.photo_tc))
async def card_photo_tc_cb(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CardStates.photo_tc)
    await callback_query.answer()
    await callback_query.message.answer(
        text='📷 Приложите фото нарушения ТС, нажмите - 📎',
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
        message_subject = f'{user_data.get("gn")} - {user_data.get("address")} ({user_data.get("phone_number")}) ' \
                          f'#{state.key.bot_id}'

        async with ChatActionSender.upload_document(
                bot=callback_query.message.bot,
                chat_id=callback_query.message.chat.id,
        ):
            # Send email
            await send_data(message_subject, user_data)

        logger.info(f'Данные успешно отправлены: {user_data}')

        await callback_query.answer(
            text='Карточка нарушения отправлена 👌',
            show_alert=True,
        )

        await init_state(state)
        await handle_card(callback_query.message, state)
    except Exception as err:
        logger.error(f'🥵 Ошибка при отправке карточки: {err}')
        await callback_query.answer(
            text=f'😢 Ошибка отправки данных карточки нарушения: {err}',
            show_alert=True,
        )
