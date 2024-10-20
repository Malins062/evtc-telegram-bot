from aiogram import Bot
from aiogram.types import (
    BotCommand,
    BotCommandScopeChatAdministrators,
    BotCommandScopeDefault,
)

from evtc_bot.config.settings import settings


async def set_user_commands(bot: Bot):
    """
    Set start bot commands for all users
    :param bot:
    :return:
    """

    commands = [
        BotCommand(
            command="start",
            description="Стартовая страница бота",
        ),
        BotCommand(
            command="help",
            description="Краткая справочная информация",
        ),
        BotCommand(
            command="card",
            description="Показать карточку нарушения, для отправки",
        ),
        BotCommand(
            command="clear",
            description="Полностью очистить карточку нарушения",
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def set_admin_commands(bot: Bot):
    """
    Set additional bot commands for admin
    :param bot:
    :return:
    """

    commands = [
        BotCommand(
            command="add_user",
            description="Открыть доступ для пользователя",
        ),
        BotCommand(
            command="remove_user",
            description="Закрыть доступ для пользователя",
        ),
        BotCommand(
            command="list_users",
            description="Вывести список разрешенных пользователей",
        ),
    ]

    await bot.set_my_commands(
        commands, BotCommandScopeChatAdministrators(chat_id=settings.admin.id)
    )
