from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from routers.card.base_handler import handle_card
from states.states import CardStates, Card, set_input_data

router = Router(name=__name__)


@router.message(CardStates.foto_protocol, F.photo)
async def handle_card_foto_protocol(message: types.Message, state: FSMContext):
    await state.update_data(foto_protocol=True)
    set_input_data(state, Card(foto_protocol=F.photo))
    await message.answer(
        text=f'✔ Фото протокола задержания добавлено.',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await handle_card(message, state)


@router.message(CardStates.foto_protocol)
async def handle_card_invalid_foto_protocol(message: types.Message):
    await message.answer(
        text=f'⛔ Вы должны приложить фотографию!',
        reply_markup=types.ReplyKeyboardRemove()
    )
