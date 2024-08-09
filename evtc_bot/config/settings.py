import os
from pathlib import Path, PosixPath, WindowsPath

from dotenv import load_dotenv
from pydantic import EmailStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()
BASE_DIR = Path(__file__).resolve().parents[1]


class LoggerSettings(BaseSettings):
    """
    Logger settings
    """

    dir: WindowsPath | PosixPath = os.getenv("DIR_LOGS", Path(BASE_DIR) / "logs")
    filename: str = os.getenv("FILE_NAME_LOG", "evtc_bot.log")
    name: str = os.getenv("LOGGER_NAME", "@EVTC_bot")


class AttachmentSettings(BaseSettings):
    """
    Settings for files & directories
    """

    dir: WindowsPath | PosixPath = os.getenv(
        "DIR_ATTACHMENTS", Path(BASE_DIR) / "attachments"
    )
    filename_data: str = os.getenv("FILE_NAME_DATA", "data.json")
    filename_protocol: str = os.getenv("FILE_NAME_IMAGE_PROTOCOL", "protocol.jpg")
    filename_tc: str = os.getenv("FILE_NAME_IMAGE_TC", "tc.jpg")
    template_card_answer: WindowsPath | PosixPath = os.getenv(
        "TEMPLATE_CARD_ANSWER",
        Path(BASE_DIR) / "templates" / "send_card_answer.html",
    )


class AdminSettings(BaseSettings):
    """
    Administrator settings
    """

    allowed_users_file: WindowsPath | PosixPath = (
        Path(BASE_DIR) / "config" / "access.usr"
    )
    phone_numbers: tuple = os.getenv("ADMIN_PHONE_NUMBERS", ("+79206328673",))
    url: str = os.getenv("ADMIN_TELEGRAM_URL", "https://t.me/Alexei_mav")
    id: int = int(os.getenv("ADMIN_TELEGRAM_ID", "200287812"))
    email: EmailStr = os.getenv("ADMIN_EMAIL", "6328673@gmail.com")


class PostageSettings(BaseSettings):
    """
    Email settings
    """

    recipient_email: EmailStr = os.getenv("EMAIL_TO", "recipient@mail.ru")
    sender_email: EmailStr = os.getenv("EMAIL_FROM", "sender@mail.ru")
    sender_pswd: str = os.getenv("EMAIL_PSWD", "password")
    sender_smtp: str = os.getenv("SMTP", "smtp.mail.ru")
    sender_port: int = int(os.getenv("PORT", "465"))
    sender_use_tls: bool = bool(os.getenv("USE_TLS", "True"))


class DBSettings(BaseSettings):
    """
    Database settings
    """

    redis_url: str = os.getenv("REDIS_URL", "redis://redis_server:6379/0")
    db_url: str = os.getenv("DB_URL", "postgresql://username:password@localhost/dbname")


class DateTimeSettings(BaseSettings):
    """
    DateTime settings
    """

    format: str = os.getenv("DT_FORMAT", "%d.%m.%Y %H:%M")
    delta: int = int(os.getenv("DT_DELTA", "8"))

    patterns: dict = {
        "date": r"^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|["
        r"2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:("
        r"?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4("
        r"?:(?:1[6-9]|[2-9]\d)?\d{2})$",
        "time": r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$",
    }


class MiddlewareSettings(BaseSettings):
    """
    Middleware settings
    """

    throttle_timeout: int = int(os.getenv("THROTTLE_TIMEOUT", "60"))
    throttle_time_interval: int = int(os.getenv("THROTTLE_TIME_INTERVAL", "500"))


class Settings(BaseSettings):
    """
    Main settings
    """

    bot_token: str = os.getenv("BOT_TOKEN")
    prefixes_command: str = os.getenv("PREFIXES_COMMAND", "!/\\")

    attachment: BaseSettings = AttachmentSettings()
    logger: BaseSettings = LoggerSettings()
    admin: BaseSettings = AdminSettings()
    postage: BaseSettings = PostageSettings()
    db: BaseSettings = DBSettings()
    dt: BaseSettings = DateTimeSettings()
    md: BaseSettings = MiddlewareSettings()

    model_config = SettingsConfigDict(
        case_sensitive=True,
    )


# Setup configuration
try:
    settings = Settings()
except ValidationError:
    pass
