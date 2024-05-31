from aiogram import Router

from .card_handler import router as card_handler_router
from .datetime_handler import router as dt_handler_router
from .gn_handler import router as gn_handler_router
from .model_handler import router as model_handler_router
from .callback_handlers import router as callback_handlers_router

router = Router(name='card')

router.include_routers(
    card_handler_router,
    dt_handler_router,
    gn_handler_router,
    model_handler_router,
    callback_handlers_router,
)
