import json
import tempfile
from datetime import datetime
from email.mime.application import MIMEApplication


def get_now() -> str:
    return datetime.now().strftime('%d.%m.%Y %H:%M')


def get_json_file(file_name: str, data: dict):
    file_data = json.dumps(data)
    json_file = tempfile.NamedTemporaryFile(mode='w')
    json_file.name = file_name
    json_file.write(file_data)

    # with open(file_name, 'w') as json_file:
    #     json_file.write(file_data)
    return json_file
