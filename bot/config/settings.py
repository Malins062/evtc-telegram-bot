import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import Secret, Field, EmailStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

# load_dotenv()
BASE_DIR = Path(__file__).resolve().parents[1]


class LoggerSettings(BaseSettings):
    """
    Logger settings
    """
    dir: str = Field(os.path.join(BASE_DIR, "logs"), env="DIR_LOGS")
    filename: str = Field("bot.log", env="FILE_NAME_LOG")
    name: str = Field("@EVTC_bot", env="LOGGER_NAME")


class AttachmentSettings(BaseSettings):
    """
    Settings for files & directories
    """
    dir: str = Field(os.path.join(BASE_DIR, "attachments"), env="DIR_ATTACHMENTS")
    data_file: str = Field("data.json", env="FILE_NAME_DATA")
    protocol_file: str = Field("protocol.jpg", env="FILE_NAME_IMAGE_PROTOCOL")
    tc_file: str = Field("tc.jpg", env="FILE_NAME_IMAGE_TC")
    template_card_answer: str = Field(
        os.path.join(BASE_DIR, "templates", "send_card_answer.html"),
        env="TEMPLATE_CARD_ANSWER"
    )


class AdminSettings(BaseSettings):
    """
    Administrator settings
    """
    allowed_users_file: str = os.path.join(BASE_DIR, "config", "access.usr")
    phone_numbers: tuple = Field(("+79206328673",), env="ADMIN_PHONE_NUMBERS")
    url: str = Field("https://t.me/Alexei_mav", env="ADMIN_TELEGRAM_URL")
    id: int = Field(200287812, env="ADMIN_TELEGRAM_ID")
    email: EmailStr = Field("6328673@gmail.com", env="ADMIN_EMAIL")


class PostageSettings(BaseSettings):
    """
    Email settings
    """
    recipient_email: EmailStr = Field(env="EMAIL_TO")
    sender_email: EmailStr = Field(env="EMAIL_FROM")
    sender_pswd: Secret[str] = Field(env="EMAIL_PSWD")
    sender_smtp: str = Field(env="SMTP")
    sender_port: int = Field(env="PORT")
    sender_use_tls: bool = Field(env="USE_TLS")


class DBSettings(BaseSettings):
    """
    Database settings
    """
    redis_url: str = Field("redis://redis_server:6379/0", env="REDIS_URL")


class Settings(BaseSettings):
    """
    Main settings
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        validate_assignment=False,
        case_sensitive=False,
        extra="forbid",
    )

    bot_token: Secret[str] = Field(env="BOT_TOKEN")
    prefixes_command: str = Field("!/\\", env="PREFIXES_COMMAND")

    base_dir: str = BASE_DIR

    attachment: AttachmentSettings()
    logger: LoggerSettings()
    admin: AdminSettings()
    postage: PostageSettings()
    db: DBSettings()

    # DateTime settings
    datetime_format: str = "%d.%m.%Y %H:%M"
    datetime_delta: int = 8

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


# Setup configuration
try:
    settings = Settings()
except ValidationError as e:
    print(e)

# Input data for card
input_data: dict = {}

# Users contact data for verification
users: dict = {}
