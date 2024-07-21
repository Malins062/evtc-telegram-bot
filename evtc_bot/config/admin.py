from pathlib import Path

from evtc_bot.config.settings import settings


def get_phones(is_all=True) -> tuple:
    phone_list = tuple
    if Path.is_file(settings.admin.allowed_users_file):
        with Path.open(settings.allowed_users_file, "r") as file:
            users_phone_numbers = file.read().splitlines()
        users_phone_numbers = list(filter(None, users_phone_numbers))
        if is_all:
            phone_list = (*users_phone_numbers, *settings.admin.phone_numbers)
        else:
            phone_list = tuple(users_phone_numbers)

    return phone_list


def save_phones(phone_list: list) -> bool:
    if Path.is_file(settings.admin.allowed_users_file):
        with Path.open(settings.admin.allowed_users_file, "w") as file:
            file.writelines("\n".join(phone_list))
            file.write("\n")
        return True

    return False


def add_phone(phone_number: str) -> bool:
    if Path.is_file(settings.admin.allowed_users_file):
        with Path.open(settings.admin.allowed_users_file, "a") as file:
            file.write(phone_number + "\n")
        return True
    return False
