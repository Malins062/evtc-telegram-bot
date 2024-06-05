from aiogram.types import (
    InlineKeyboardMarkup, ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


class CommonButtonsText:
    CONFIRM = '✔ Подтверждаю'
    CANCEL = '✖ Отмена'
    CONTACT = 'Отправить свой контакт ☎'


def build_confirm_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=CommonButtonsText.CONFIRM)
    builder.button(text=CommonButtonsText.CANCEL)
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def build_request_contact_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(
        text=CommonButtonsText.CONTACT,
        request_contact=True,
    )
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def build_values_keyboard(list_values: [], sizes=None) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for text in list_values:
        builder.button(text=text)
    builder.adjust(sizes if sizes else 3, repeat=True)

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
    )
