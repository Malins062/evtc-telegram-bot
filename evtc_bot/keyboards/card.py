from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardMarkup,
)
from aiogram.utils import markdown
from aiogram.utils.keyboard import InlineKeyboardBuilder

SEND_BUTTON = "send"


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


class CardCbData(CallbackData, prefix="card"):
    action: CardActions


class CardButton:
    def __init__(self, title: str, annotation: str, action: CardActions):
        self.title = title
        self.annotation = annotation
        self.action = action


CARD_BUTTONS = {
    "dt": CardButton(
        "📅 ДАТА И ВРЕМЯ", "указать дату и время нарушения", CardActions.dt
    ),
    "address": CardButton(
        "🌍 МЕСТО", "указать адрес правонарушения", CardActions.address
    ),
    "gn": CardButton(
        "🚘 НОМЕР ТС", "изменить гос.номер, задерживаемого ТС", CardActions.gn
    ),
    "model": CardButton("🚗 МАРКА", "изменить модель ТС", CardActions.model),
    "parking": CardButton(
        "🏁 СТОЯНКА",
        "указать штраф-стоянку, на которую помещено ТС",
        CardActions.parking,
    ),
    "article": CardButton(
        "👩‍⚖️ СТАТЬЯ КОАП РФ", "указать статью КоАП РФ", CardActions.article
    ),
    "protocol": CardButton(
        "📃 ПРОТОКОЛ", "изменить номер протокола задержания ТС", CardActions.protocol
    ),
    "photo_protocol": CardButton(
        "📷 ФОТО ПРОТОКОЛА",
        "сделать фото протокола задержания ТС",
        CardActions.photo_protocol,
    ),
    "photo_tc": CardButton(
        "📷 ФОТО ТС", "сделать фото нарушения ТС", CardActions.photo_tc
    ),
    SEND_BUTTON: CardButton(
        "📩 ОТПРАВИТЬ", "отправить заполненные сведения", CardActions.send
    ),
}


def get_annotations_card_buttons() -> str:
    text = ""
    for btn in CARD_BUTTONS:
        text += markdown.text(
            f"{CARD_BUTTONS[btn].title} - {markdown.hitalic(CARD_BUTTONS[btn].annotation)} \n"
        )
    return text


def build_card_keyboard(is_valid_card: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for btn in CARD_BUTTONS:
        if (btn != SEND_BUTTON) or ((btn == SEND_BUTTON) and is_valid_card):
            builder.button(
                text=CARD_BUTTONS[btn].title,
                callback_data=CardCbData(action=CARD_BUTTONS[btn].action).pack(),
            )

    builder.adjust(2, 3, 2, 2)
    return builder.as_markup(resize_keyboard=True)
