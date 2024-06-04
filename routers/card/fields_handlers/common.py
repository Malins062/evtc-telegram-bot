import os

from aiogram import types

from config_data.config import settings
from utils.common import create_download_dir


async def download_photo(message: types.Message, base_filename: str):
    if message.photo:
        create_download_dir()
        file_id = message.photo[-1].file_id
        photo_file = await message.bot.get_file(file_id)
        file_name = f'{base_filename}{os.path.splitext(photo_file.file_path)[1]}'
        photo_path = os.path.join(settings.attachments_dir, file_name)
        await message.bot.download(file_id, photo_path)

        return file_name
