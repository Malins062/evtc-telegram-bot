from pathlib import Path

from aiogram import types

from evtc_bot.config.settings import settings


async def download_photo(message: types.Message, base_filename: str):
    if message.photo:
        Path.mkdir(settings.attachment.dir, parents=True, exist_ok=True)
        file_id = message.photo[-1].file_id
        # photo_file = await message.evtc_bot.get_file(file_id)
        # file_name = f'{base_filename}{os.path.splitext(photo_file.file_path)[1]}'
        # file_name = f'{base_filename}{os.path.splitext(photo_file.file_path)[1]}'
        photo_path = Path(settings.attachment.dir) / base_filename
        await message.bot.download(file_id, photo_path)

        return base_filename
