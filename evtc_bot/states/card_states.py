from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils import markdown

from evtc_bot.config.settings import settings
from evtc_bot.db.redis.models import StrType, User, UserData
from evtc_bot.utils.bot_files import delete_files_startswith
from evtc_bot.utils.common import get_now

EMPTY = "пусто"


class CardStates(StatesGroup):
    dt = State()
    article = State()
    gn = State()
    model = State()
    address = State()
    protocol = State()
    parking = State()
    photo_protocol = State()
    photo_tc = State()


class PhotoStates(StatesGroup):
    tc = CardStates.photo_tc
    protocol = CardStates.photo_protocol


async def update_user_data(user_id: int, values: UserData):
    user = await User.get_from_redis(user_id)
    values_to_update = {
        **user.data.dict(),
        **values.dict(exclude_unset=True),
    }
    data = UserData(**values_to_update)

    user = User(
        id=user_id,
        name=user.name,
        phone_number=user.phone_number,
        data=data,
    )

    await user.save_to_redis()


async def init_state(
    state: FSMContext, name: StrType = None, phone_number: StrType = None
) -> FSMContext:
    user_id = state.key.user_id

    user = await User.get_from_redis(user_id)
    if user:
        name = user.name
        phone_number = user.phone_number

    data = get_init_user_data()

    # Creating or replacing user with initial params
    user = User(
        id=user_id,
        name=name,
        phone_number=phone_number,
        data=data,
    )

    # Save user to Redis
    await user.save_to_redis()

    # Removing all temporary files
    delete_files_startswith(str(user_id))

    new_state = state
    await new_state.clear()

    return new_state


async def reset_state(state: FSMContext) -> FSMContext:
    current_state = await state.get_state()
    if current_state:
        await state.set_state(None)
    return state


def validate_card(data: UserData) -> bool:
    values = data.dict()
    return all(values.values())


def get_init_user_data():
    data = UserData(
        dt=get_now(settings.dt.format),
        protocol="АВ123456",
        gn="В062ВВ62",
        article="article",
        address="address",
        parking="parking",
        model="model",
    )
    return data


def get_validate_symbol(is_valid: bool) -> str:
    return "✔" if is_valid else "❌"


def get_value_card_text(value, display_value=True):
    value = value if value else EMPTY
    result = get_validate_symbol(value != EMPTY)
    if display_value:
        result += (
            f" {markdown.hitalic(value)}"
            if value == EMPTY
            else f" {markdown.hbold(value)}"
        )
    return result


def get_card_text(user: User) -> str:
    data = user.data
    text = markdown.text(
        markdown.hbold(
            f"🚔 КАРТОЧКА НАРУШЕНИЯ {get_validate_symbol(validate_card(data))}"
        ),
        markdown.hbold(f"(👮‍♂️ - 📱{user.phone_number})"),
        "",
        f"Дата и время: {get_value_card_text(data.dt)}",
        f"Адрес: {get_value_card_text(data.address)}",
        markdown.text(
            f"Номер ТС: {get_value_card_text(data.gn)}. ",
            f"Марка, модель: {get_value_card_text(data.model)}",
        ),
        f"Статья КоАП РФ: {get_value_card_text(data.article)}",
        f"Протокол: {get_value_card_text(data.protocol)}",
        f"Стоянка: {get_value_card_text(data.parking)}",
        markdown.text(
            f"Фото протокола: {get_value_card_text(data.photo_protocol, display_value=False)} ",
            f"Фото ТС: {get_value_card_text(data.photo_tc, display_value=False)}",
        ),
        "",
        sep="\n",
    )
    return text
