from aiogram.types import (
    InlineKeyboardMarkup, ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from utils.common import get_now


class CommonButtonText:
    CONFIRM = '✔ Подтверждаю'
    CANCEL = '✖ Отмена'


def build_confirm_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=CommonButtonText.CONFIRM)
    builder.button(text=CommonButtonText.CANCEL)
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def build_values_keyboard(list_values: []) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for text in list_values:
        builder.button(text=text)
    if len(list_values) > 3:
        builder.adjust(3, repeat=True)

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
    )
