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
    clear = auto()
    send = auto()


class CardCbData(CallbackData, prefix='card'):
    action: CardActions


class CardButtonText:
    DT = '📅 ДАТА И ВРЕМЯ'
    ADDRESS = '🌍 МЕСТО'
    GN = '🚘 НОМЕР ТС'
    MODEL = '🚗 МОДЕЛЬ ТС'
    ARTICLE = '👩‍⚖️ СТАТЬЯ КОАП РФ'
    PROTOCOL = '📃 ПРОТОКОЛ'
    PARKING = '🏁 СТОЯНКА'
    SEND = '📩 ОТПРАВИТЬ'
    CLEAR = '🧹 ОЧИСТИТЬ'


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
        text=CardButtonText.ARTICLE,
        callback_data=CardCbData(action=CardActions.article).pack(),
    )
    builder.button(
        text=CardButtonText.PROTOCOL,
        callback_data=CardCbData(action=CardActions.protocol).pack(),
    )
    builder.button(
        text=CardButtonText.PARKING,
        callback_data=CardCbData(action=CardActions.parking).pack(),
    )
    builder.button(
        text=CardButtonText.CLEAR,
        callback_data=CardCbData(action=CardActions.clear).pack(),
    )

    if is_valid_card:
        builder.button(
            text=CardButtonText.SEND,
            callback_data=CardCbData(action=CardActions.send).pack(),
        )

    builder.adjust(2, 2, 2, 1, 1)
    return builder.as_markup(resize_keyboard=True)
