__all__ = ('router', )

from aiogram import Router

# from .admin_handlers import router as admin_router
from .commands import router as commands_router
from .card import router as card_router
# from .common import router as common_router
# from .media_handlers import router as media_router

router = Router(name=__name__)

router.include_routers(
    commands_router,
    card_router,
    # media_router,
    # admin_router,
)
