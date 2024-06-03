from aiogram import Router

from routers.card.fields_handlers.datetime import router as dt_handler_router
from routers.card.fields_handlers.gn import router as gn_handler_router
from routers.card.fields_handlers.model import router as model_handler_router
from routers.card.fields_handlers.protocol import router as protocol_handler_router
from routers.card.fields_handlers.article import router as article_handler_router
from routers.card.fields_handlers.parking import router as parking_handler_router

router = Router(name=__name__)

router.include_routers(
    dt_handler_router,
    gn_handler_router,
    model_handler_router,
    protocol_handler_router,
    article_handler_router,
    parking_handler_router,
)
