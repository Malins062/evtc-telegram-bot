from aiogram import Router

from .card_handler import router as card_handler_router
from routers.card.fields_handlers import router as fields_handlers_router
from .callback_handlers import router as callback_handlers_router

router = Router(name='card')

router.include_routers(
    card_handler_router,
    fields_handlers_router,
    callback_handlers_router,
)
