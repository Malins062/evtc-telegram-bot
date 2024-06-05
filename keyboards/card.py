from enum import auto, IntEnum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


class CardActions(IntEnum):
    dt = auto()
    address = auto()
    gn = auto()
    model = auto()
    article = auto()
    protocol = auto()
    parking = auto()
    photo_protocol = auto()
    photo_tc = auto()
    send = auto()


class CardCbData(CallbackData, prefix='card'):
    action: CardActions


class CardButtonText:
    DT = '📅 ДАТА И ВРЕМЯ'
    ADDRESS = '🌍 МЕСТО'
    GN = '🚘 НОМЕР ТС'
    MODEL = '🚗 МАРКА'
    PARKING = '🏁 СТОЯНКА'
    ARTICLE = '👩‍⚖️ СТАТЬЯ КОАП РФ'
    PROTOCOL = '📃 ПРОТОКОЛ'
    PHOTO_PROTOCOL = '📷 ФОТО ПРОТОКОЛА'
    PHOTO_TC = '📷 ФОТО ТС'
    SEND = '📩 ОТПРАВИТЬ'


def build_card_keyboard(is_valid_card: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=CardButtonText.DT,
        callback_data=CardCbData(action=CardActions.dt).pack(),
    )
    builder.button(
        text=CardButtonText.ADDRESS,
        callback_data=CardCbData(action=CardActions.address).pack(),
        request_location=True,
    )
    builder.button(
        text=CardButtonText.GN,
        callback_data=CardCbData(action=CardActions.gn).pack(),
    )
    builder.button(
        text=CardButtonText.MODEL,
        callback_data=CardCbData(action=CardActions.model).pack(),
    )
    builder.button(
        text=CardButtonText.PARKING,
        callback_data=CardCbData(action=CardActions.parking).pack(),
    )
    builder.button(
        text=CardButtonText.ARTICLE,
        callback_data=CardCbData(action=CardActions.article).pack(),
    )
    builder.button(
        text=CardButtonText.PROTOCOL,
        callback_data=CardCbData(action=CardActions.protocol).pack(),
    )

    builder.button(
        text=CardButtonText.PHOTO_PROTOCOL,
        callback_data=CardCbData(action=CardActions.photo_protocol).pack(),
    )
    builder.button(
        text=CardButtonText.PHOTO_TC,
        callback_data=CardCbData(action=CardActions.photo_tc).pack(),
    )

    if is_valid_card:
        builder.button(
            text=CardButtonText.SEND,
            callback_data=CardCbData(action=CardActions.send).pack(),
        )

    builder.adjust(2, 3, 2, 2)
    return builder.as_markup(resize_keyboard=True)
