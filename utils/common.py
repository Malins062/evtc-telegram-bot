import json
import tempfile
from datetime import datetime

from config_data.config import settings


def get_now() -> str:
    return datetime.now().strftime('%d.%m.%Y %H:%M')


def get_json_file(data: dict) -> str:
    file_data = json.dumps(data, ensure_ascii=False, indent=4)
    file = tempfile.NamedTemporaryFile(mode='w',
                                       prefix=f'{data.get("user_id")}-json-',
                                       dir=settings.attachments_dir,
                                       delete=False)
    try:
        file.write(file_data)
    finally:
        file.close()
        return file.name
