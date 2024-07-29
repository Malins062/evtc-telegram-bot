import json
import logging
import os.path
import re
from pathlib import Path

from evtc_bot.config.settings import settings
from evtc_bot.db.redis.models import User

logger = logging.getLogger(__name__)


def get_prefix_file_name(user: User) -> str:
    prefix_file_name = user.phone_number + user.data.dt
    prefix_file_name = "".join(re.findall(r"[0-9]+", prefix_file_name)) + "_"
    return prefix_file_name


def create_json_data_file(user: User) -> str | Exception:
    try:
        Path.mkdir(settings.attachment.dir, parents=True, exist_ok=True)
        filename = f"{user.id}-{settings.attachment.filename_data}"
        full_filename = Path(settings.attachment.dir) / filename

        prefix = get_prefix_file_name(user)
        user.data.photo_protocol = prefix + settings.attachment.filename_protocol
        user.data.photo_tc = prefix + settings.attachment.filename_tc

        data = {
            **user.dict(by_alias=True, exclude={user.role, user.data, user.name, user.id}),
            **user.data.dict(),
        }
        with Path.open(full_filename, "w") as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
        return outfile.name
    except Exception as err:
        error_text = "Ошибка при создании json-файла"
        logger.error(f"{error_text}: {err}")
        return err


def delete_files_startswith(start_name: str):
    try:
        deleted_files = []
        for file_name in os.listdir(settings.attachment.dir):
            if file_name.startswith(start_name):
                file_to_delete = Path(settings.attachment.dir) / file_name
                Path.unlink(file_to_delete)
                deleted_files.append(file_to_delete)
        return deleted_files
    except Exception as err:
        error_text = "Ошибка при удалении временных файлов"
        logger.error(f"{error_text}: {err}")
        return str(err)
