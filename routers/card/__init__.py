from aiogram import Router

from .handlers import router as handlers_router
from .callback_handlers import router as callback_handlers_router

router = Router(name='card')
router.include_routers(
    handlers_router,
    callback_handlers_router,
)
