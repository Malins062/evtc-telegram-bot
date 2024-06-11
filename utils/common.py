import json
import os.path
import datetime as dt
import re

from config_data.config import settings


def get_now(utc=settings.time_utc) -> str:
    now = dt.datetime.now()
    now += dt.timedelta(hours=utc)
    return now.strftime('%d.%m.%Y %H:%M')


def create_download_dir():
    if not os.path.exists(settings.attachments_dir):
        os.makedirs(settings.attachments_dir)


def get_prefix_file_name(data: dict) -> str:
    prefix_file_name = data.get('phone_number') + data.get('dt')
    prefix_file_name = ''.join(re.findall(r'[0-9]+', prefix_file_name)) + '_'
    return prefix_file_name


def create_json_data_file(data: dict) -> str | Exception:
    try:
        create_download_dir()
        filename = f'{data.get("user_id")}-{settings.data_file}'
        full_filename = os.path.join(settings.attachments_dir, filename)
        prefix = get_prefix_file_name(data)
        data['photo_protocol'] = prefix + settings.protocol_file
        data['photo_tc'] = prefix + settings.tc_file

        with open(full_filename, 'w') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
    except Exception as err:
        return err
    finally:
        outfile.close()
        return outfile.name


def delete_files_startswith(start_name: str):
    try:
        deleted_files = []
        for file_name in os.listdir(settings.attachments_dir):
            if file_name.startswith(start_name):
                file_to_delete = os.path.join(settings.attachments_dir, file_name)
                os.remove(file_to_delete)
                deleted_files.append(file_to_delete)
        return deleted_files
    except Exception as err:
        return err
