from aiogram import F, Router, types
from aiogram.enums import ChatAction
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

from evtc_bot.config.settings import settings
from evtc_bot.db.redis.models import UserData
from evtc_bot.handlers.card.base_handlers import handle_card
from evtc_bot.handlers.card.fields_handlers.common import download_photo
from evtc_bot.states.card_states import PhotoStates, update_user_data

router = Router(name=__name__)


@router.message(StateFilter(PhotoStates), F.photo)
async def handle_card_photo_tc(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == "PhotoStates:photo_tc":
        param_name = "photo_tc"
        settings_file_name = settings.attachment.filename_tc
        message_text = "нарушения ТС"
    else:
        param_name = "photo_protocol"
        settings_file_name = settings.attachment.filename_protocol
        message_text = "протокола задержания"

    await state.update_data(**{param_name: True})
    filename = f"{state.key.user_id}-{settings_file_name}"

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    )

    async with ChatActionSender.upload_photo(
        bot=message.bot,
        chat_id=message.chat.id,
    ):
        await download_photo(message, filename)

    await update_user_data(
        state.key.user_id, UserData(**{param_name: settings_file_name})
    )

    await message.answer(
        text=f"✔ Фото {message_text} добавлено.",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await handle_card(message, state)


@router.message(StateFilter(PhotoStates))
async def handle_card_invalid_photo_tc(message: types.Message):
    await message.reply(
        text="⛔ Вы должны приложить фотографию!",
        reply_markup=types.ReplyKeyboardRemove(),
    )
