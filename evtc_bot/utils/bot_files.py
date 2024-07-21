import json
import os.path
import re
from pathlib import Path

from evtc_bot.config.settings import settings


def get_prefix_file_name(data: dict) -> str:
    prefix_file_name = data.get("phone_number") + data.get("dt")
    prefix_file_name = "".join(re.findall(r"[0-9]+", prefix_file_name)) + "_"
    return prefix_file_name


def create_json_data_file(data: dict) -> str | Exception:
    try:
        Path.mkdir(settings.attachment.dir)
        filename = f'{data.get("user_id")}-{settings.attachment.filename_data}'
        full_filename = Path(settings.attachment.dir) / filename
        prefix = get_prefix_file_name(data)
        data["photo_protocol"] = prefix + settings.attachment.filename_protocol
        data["photo_tc"] = prefix + settings.attachment.filename_tc

        with Path.open(full_filename, "w") as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
        return outfile.name
    except Exception as err:
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
        return err
