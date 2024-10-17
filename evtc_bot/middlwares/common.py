from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.redis import RedisStorage


async def get_current_state(storage: RedisStorage, user_id: int, bot_id: int):
    """
    Get FSM state_key from storage for user_id, and bot_id
    :param storage: storage
    :param user_id: user id
    :param bot_id: bot id
    :return: state and state_key
    """

    state_key: StorageKey = StorageKey(
        chat_id=user_id,
        user_id=user_id,
        bot_id=bot_id,
    )
    state = await storage.get_state(state_key)
    return state, state_key
