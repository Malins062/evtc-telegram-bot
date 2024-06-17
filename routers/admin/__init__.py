from aiogram import Router

from .admin_commands import router as admin_commands_router
from .actions_handler import router as actions_handler_router
from .contact_handler import router as phone_handler_router


router = Router(name='admin')

router.include_routers(
    admin_commands_router,
    actions_handler_router,
    phone_handler_router,
)
