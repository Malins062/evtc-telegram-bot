from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from evtc_bot.handlers.card.base_handlers import handle_card

router = Router(name=__name__)


@router.message()
async def echo_message(message: types.Message, state: FSMContext):
    await message.reply(
        text=f"😢️️ {markdown.hbold(message.from_user.full_name)}, я Вас не понимаю!"
    )
    await handle_card(message, state)

    # if not users.get(state.key.user_id):
    #     await handle_card(message, state)
