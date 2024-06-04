import json
import os.path
from datetime import datetime

from config_data.config import settings


def get_now() -> str:
    return datetime.now().strftime('%d.%m.%Y %H:%M')


def get_json_file(data: dict) -> str | Exception:
    try:
        filename = f'{data.get("user_id")}-{settings.data_file}'
        full_filename = os.path.join(settings.attachments_dir, filename)
        with open(full_filename, 'w') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
    except Exception as err:
        return err
    finally:
        outfile.close()
        return outfile.name
