__all__ = ("router",)

from aiogram import Router

from ..db.redis.engine import redis_storage as storage
from ..middlwares.state_contact import CheckContactStateMiddleware

# from .admin import router as admin_commands_router
from .base_commands import router as base_commands_router
from .card import router as card_commands_router
from .contact_handler import router as contact_router
from .user_commands import router as user_commands_router

router = Router(name=__name__)

# Set filter middleware for user get contact
base_commands_router.message.middleware(CheckContactStateMiddleware(storage))
base_commands_router.callback_query.middleware(CheckContactStateMiddleware(storage))
card_commands_router.message.middleware(CheckContactStateMiddleware(storage))
card_commands_router.callback_query.middleware(CheckContactStateMiddleware(storage))
user_commands_router.message.middleware(CheckContactStateMiddleware(storage))

router.include_routers(
    base_commands_router,
    contact_router,
    # admin_commands_router,
    card_commands_router,
    user_commands_router,
)
