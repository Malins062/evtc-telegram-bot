from pathlib import Path

from aiogram import types

from evtc_bot.config.settings import settings
from evtc_bot.utils.bot_files import create_dir


async def download_photo(message: types.Message, base_filename: str):
    if message.photo:
        create_dir(settings.attachment.dir)
        file_id = message.photo[-1].file_id
        # photo_file = await message.evtc_bot.get_file(file_id)
        # file_name = f'{base_filename}{os.path.splitext(photo_file.file_path)[1]}'
        # file_name = f'{base_filename}{os.path.splitext(photo_file.file_path)[1]}'
        photo_path = Path(settings.dir) / base_filename
        await message.bot.download(file_id, photo_path)

        return base_filename
