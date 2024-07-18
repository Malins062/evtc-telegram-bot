import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()
BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
    )

    bot_token: str = os.getenv("BOT_TOKEN")

    # Files & directories
    attachments_dir: str = os.path.join(BASE_DIR, "attachments")
    logs_dir: str = os.path.join(BASE_DIR, "logs")
    template_card_answer: str = os.path.join(
        BASE_DIR, "templates", "send_card_answer.html"
    )
    log_file: str = "bot.log"
    data_file: str = "data.json"
    protocol_file: str = "protocol.jpg"
    tc_file: str = "tc.jpg"

    logger_name: str = "EVTC_bot"

    # Admin settings
    allowed_users_file: str = os.path.join(BASE_DIR, "config", "access.usr")
    admin_phone_numbers: tuple = ("+79206328673",)
    admin_url: str = "https://t.me/Alexei_mav"
    admin_id: int = 200287812
    email_admin: str = "6328673@gmail.com"

    # Email settings
    email_to: str = os.getenv("EMAIL_TO")
    email_from: str = os.getenv("EMAIL_FROM")
    email_pswd: str = os.getenv("EMAIL_PSWD")
    smtp: str = os.getenv("SMTP")
    port: int = os.getenv("PORT")
    use_tls: bool = os.getenv("USE_TLS")

    # Databases
    # redis_host: str = os.getenv("REDIS_HOST")
    # redis_pswd: str = os.getenv("REDIS_PSWD")
    # redis_user: str = os.getenv("REDIS_USER")
    # redis_user_pswd: str = os.getenv("REDIS_USER_PSWD")

    # DateTime settings
    datetime_format: str = "%d.%m.%Y %H:%M"
    datetime_delta: int = 8

    prefix: str = "!/\\"

    select_values: dict = {
        "model": (
            "ВАЗ",
            "КИА",
            "ШКОДА",
            "HYUNDAI",
            "МЕРСЕДЕС",
            "ТОЙОТА",
            "ЛЕКСУС",
            "БМВ",
            "HONDA",
            "GEELY",
            "HAVAL",
            "РЕНО",
        ),
        "gn": ("БН",),
        "article": {
            "ЗНАК 3.27": "ОСТАНОВКА ТС В ЗОНЕ ДЕЙСТВИЯ ЗНАКА 3.27 (П.П.1.3) СТ.12.16 Ч.4",
            "ПЕШЕХОДНЫЙ ПЕРЕХОД": "ОСТАНОВКА НА ПЕШЕХОДНОМ ПЕРЕХОДЕ ИЛИ БЛИЖЕ 5М ПЕРЕД НИМ (П.П.12.4) СТ.12.9 Ч.3",
            "ТРОТУАР 6.4": "ОСТАНОВКА ТС НА ТРОТУАРЕ ПРИ ОТСУТСТВИИ ЗНАКА 6.4 (П.П.12.2) СТ.12.9 Ч.3",
            "ИНВАЛИД 3.28": 'СТОЯНКА ТС БЕЗ ТАБЛИЧКИ "ИНВАЛИД" В ЗОНЕ ДЕЙСТВИЯ ЗНАКА 3.28 СТ.12.16 Ч.4',
            "ИНВАЛИД 3.29": 'СТОЯНКА ТС БЕЗ ТАБЛИЧКИ "ИНВАЛИД" В ЗОНЕ ДЕЙСТВИЯ ЗНАКА 3.29 СТ.12.16 Ч.4',
            "ИНВАЛИД 3.30": 'СТОЯНКА ТС БЕЗ ТАБЛИЧКИ "ИНВАЛИД" В ЗОНЕ ДЕЙСТВИЯ ЗНАКА 3.30 СТ.12.16 Ч.4',
            "ИНВАЛИД 6.4": 'СТОЯНКА ТС БЕЗ ТАБЛИЧКИ "ИНВАЛИД" В ЗОНЕ ДЕЙСТВИЯ ЗНАКА 6.4 (П.П.1.3) СТ.12.19 Ч.2',
            "ДАЛЕЕ 1-ГО РЯДА": "ОСТАНОВКА/СТОЯНКА ТС ДАЛЕЕ 1-ГО РЯДА КРАЯ ПРОЕЗЖЕЙ ЧАСТИ (П.П.12.2) СТ.12.19 Ч.2",
            "СОЗДАНИЕ ПОМЕХ": "ОСТАНОВКА/СТОЯНКА ТС, КОТОРОЕ ПОВЛЕКЛО СОЗДАНИЕ ПОМЕХ ДЛЯ ДРУГИХ ТС (П.П.12.4) СТ.12.19 Ч.3.2",
            "ООТ": "ОСТАНОВКА ТС, БЛИЖЕ 15М ОТ ООТ ЛИБО В МЕСТЕ ООТ (П.П.12.4) СТ.12.19 Ч.4",
        },
        "parking": {
            "СОЛНЕЧНАЯ": "ООО КПФ ДИНАМО, ул.СОЛНЕЧНАЯ Д.1А, тел.8-930-783-33-02",
            "ОКСКИЙ ПР-Д": "ИП Платонов, ОКСКИЙ ПРОЕЗД Д.15, тел.8-977-466-65-75, 40-70-74",
            "ТОВАРНЫЙ ДВОР": "ООО АвтоТрансСервис 62, ул.ТОВАРНЫЙ ДВОР Д.60, тел.8-920-955-44-44",
            "СЕМИНАРСКАЯ": "МП МКЦ, ул.СЕМИНАРСКАЯ Д.49, тел.8-900-606-03-05",
            "КОСТЫЧЕВА": "ООО СпецТрансМО, ул.КОСТЫЧЕВА Д.15Б СТР.4, тел.8-960-603-44-62",
            "ГОРЬКОГО": "ООО СпецТрансМО, ул.ГОРЬКОГО Д.1 СТР.2, тел.8-960-603-44-62",
        },
    }

    patterns: dict = {
        "date": r"^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|["
        r"2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:("
        r"?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4("
        r"?:(?:1[6-9]|[2-9]\d)?\d{2})$",
        "time": r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$",
    }


# Configuration
settings = Settings()

# Input data for card
input_data: dict = {}

# Users contact data for verification
users: dict = {}
