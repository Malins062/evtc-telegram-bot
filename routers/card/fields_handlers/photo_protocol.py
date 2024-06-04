from aiogram import Router, types, F
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

from routers.card.base_handler import handle_card
from routers.card.fields_handlers.common import download_photo
from states.states import CardStates, Card, set_input_data

router = Router(name=__name__)


@router.message(CardStates.photo_protocol, F.photo)
async def handle_card_photo_protocol(message: types.Message, state: FSMContext):
    await state.update_data(photo_protocol=True)
    filename = f'{state.key.user_id}-protocol'

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    )

    async with ChatActionSender.upload_document(
            bot=message.bot,
            chat_id=message.chat.id,
    ):
        full_filename = await download_photo(message, filename)

    set_input_data(state, Card(photo_protocol=full_filename))

    await message.answer(
        text=f'✔ Фото протокола задержания добавлено.',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await handle_card(message, state)


@router.message(CardStates.photo_protocol)
async def handle_card_invalid_photo_protocol(message: types.Message):
    await message.answer(
        text=f'⛔ Вы должны приложить фотографию!',
        reply_markup=types.ReplyKeyboardRemove()
    )
