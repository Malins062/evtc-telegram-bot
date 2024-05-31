from enum import auto, IntEnum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


class CardActions(IntEnum):
    dt = auto()
    gn = auto()
    model = auto()
    article = auto()
    address = auto()
    protocol = auto()
    clear = auto()
    send = auto()


class CardCbData(CallbackData, prefix='card'):
    action: CardActions


class CardButtonText:
    DT = '📅 ДАТА И ВРЕМЯ'
    GN = '🚘 НОМЕР ТС'
    MODEL = '🚗 МОДЕЛЬ ТС'
    ARTICLE = '👩‍⚖️ СТАТЬЯ КОАП РФ'
    ADDRESS = '🗺 МЕСТО НАРУШЕНИЯ'
    PROTOCOL = '📃 ПРОТОКОЛ'
    SEND = '📩 ОТПРАВИТЬ'
    CLEAR = '🧹 ОЧИСТИТЬ'


def build_card_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=CardButtonText.DT,
        callback_data=CardCbData(action=CardActions.dt).pack(),
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
        text=CardButtonText.ADDRESS,
        callback_data=CardCbData(action=CardActions.address).pack(),
        request_location=True,
    )
    builder.button(
        text=CardButtonText.CLEAR,
        callback_data=CardCbData(action=CardActions.clear).pack(),
    )
    builder.button(
        text=CardButtonText.SEND,
        callback_data=CardCbData(action=CardActions.send).pack(),
    )

    builder.adjust(1, 2, 2, 1, 1, 1)
    return builder.as_markup(resize_keyboard=True)
