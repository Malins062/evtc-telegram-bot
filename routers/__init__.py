__all__ = ('router', )

from aiogram import Router

from .base_commands import router as base_commands_router
from .user_commands import router as user_commands_router
from .card import router as card_router

router = Router(name=__name__)

router.include_routers(
    base_commands_router,
    card_router,
    user_commands_router,
)
