from aiogram import Router

from evtc_bot.handlers.card.fields_handlers.datetime import router as dt_handler_router
from evtc_bot.handlers.card.fields_handlers.gn import router as gn_handler_router
from evtc_bot.handlers.card.fields_handlers.model import router as model_handler_router
from evtc_bot.handlers.card.fields_handlers.protocol import router as protocol_handler_router
from evtc_bot.handlers.card.fields_handlers.article import router as article_handler_router
from evtc_bot.handlers.card.fields_handlers.parking import router as parking_handler_router
from evtc_bot.handlers.card.fields_handlers.address import router as address_handler_router
from evtc_bot.handlers.card.fields_handlers.photo import router as photo_handler_router

router = Router(name=__name__)

router.include_routers(
    dt_handler_router,
    gn_handler_router,
    model_handler_router,
    protocol_handler_router,
    article_handler_router,
    parking_handler_router,
    address_handler_router,
    photo_handler_router,
)
