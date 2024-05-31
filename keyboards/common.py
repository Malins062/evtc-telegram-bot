from aiogram.types import (
    InlineKeyboardMarkup, ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


class CommonButtonText:
    CONFIRM = '✔ Подтверждаю'
    CANCEL = '✖ Отмена'


class ValuesButtonText:
    BN = 'БН'


def build_confirm_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=CommonButtonText.CONFIRM)
    builder.button(text=CommonButtonText.CANCEL)
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def build_gn_values_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=ValuesButtonText.BN)
    builder.adjust(1)
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
    )
