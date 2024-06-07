from aiogram import Router, types, F
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

from config_data.config import settings
from routers.card.base_handler import handle_card
from routers.card.fields_handlers.common import download_photo
from states.states import CardStates, Card, set_input_data

router = Router(name=__name__)


@router.message(CardStates.photo_tc, F.photo)
async def handle_card_photo_tc(message: types.Message, state: FSMContext):
    await state.update_data(photo_tc=True)
    filename = f'{state.key.user_id}-{settings.tc_file}'

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    )

    async with ChatActionSender.upload_photo(
            bot=message.bot,
            chat_id=message.chat.id,
    ):
        await download_photo(message, filename)

    set_input_data(state, Card(photo_tc=settings.tc_file))

    await message.answer(
        text=f'✔ Фото нарушения ТС добавлено.',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await handle_card(message, state)


@router.message(CardStates.photo_tc)
async def handle_card_invalid_photo_tc(message: types.Message):
    await message.answer(
        text=f'⛔ Вы должны приложить фотографию!',
        reply_markup=types.ReplyKeyboardRemove()
    )
