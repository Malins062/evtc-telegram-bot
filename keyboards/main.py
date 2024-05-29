from aiogram.types import (
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class MainButtonText:
    CARD = '🚔 КАРТОЧКА НАРУШЕНИЯ'
    SEND = '📩 ОТПРАВИТЬ'
    CLEAR = '🧹 ОЧИСТИТЬ'


def build_main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=MainButtonText.CARD)
    builder.button(text=MainButtonText.SEND)
    builder.button(text=MainButtonText.CLEAR)
    builder.adjust(1, 2)
    return builder.as_markup(resize_keyboard=True)
