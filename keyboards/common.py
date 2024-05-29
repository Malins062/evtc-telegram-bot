from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButtonPollType, InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


class CommonButtonText:
    CONFIRM = '👌 Подтверждаю'
    CANCEL = '✖ Отмена'


def build_confirm_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=CommonButtonText.CONFIRM)
    builder.button(text=CommonButtonText.CANCEL)
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
