from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from validators.card import validate_model
from routers.card.base_handler import handle_card
from states.states import CardStates, set_input_data, Card

router = Router(name=__name__)


@router.message(CardStates.model, F.text.cast(validate_model).as_('model'))
async def handle_card_model(message: types.Message, state: FSMContext, model: str):
    await state.update_data(model=True)
    set_input_data(state, Card(model=model))
    await message.answer(
        text=f'✔ Модель ТС изменена на - {markdown.hbold(model)}',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await handle_card(message, state)


@router.message(CardStates.model)
async def handle_card_invalid_model(message: types.Message):
    await message.answer(
        text=markdown.text(
            f'⛔ Ошибочный формат модели ТС - "{markdown.hbold(message.text)}"',
            'Модель ТС должна быть в диапазоне 2-25 символов!',
            sep='\n',
        )
    )
