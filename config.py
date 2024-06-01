import os
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
    )

    bot_token: str = os.getenv('BOT_TOKEN')
    log_file: str = os.getenv('LOG_FILE')
    prefix: str = '!/\\'

    email_to: str = os.getenv('EMAIL_TO')
    email_from: str = os.getenv('EMAIL_FROM')
    email_pswd: str = os.getenv('EMAIL_PSWD')
    smtp: str = os.getenv('SMTP')
    port: int = os.getenv('PORT')
    use_tls: bool = os.getenv('USE_TLS')

    select_values: dict = {
        'model': ['ВАЗ', 'КИА', 'HYUNDAI', 'МЕРСЕДЕС', 'ТОЙОТА', 'ЛЕКСУС', 'БМВ', 'HONDA', 'GEELY', 'HAVAL'],
        'gn': ['БН'],
    }

    patterns: dict = {
        'date': r'^(?:(?:(?:0?[13578]|1[02])(\/|-|\.)31)\1|(?:(?:0?[1,3-9]|1[0-2])(\/|-|\.)(?:29|30)\2))(?:(?:1['
                r'6-9]|[2-9]\d)?\d{2})$|^(?:0?2(\/|-|\.)29\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579]['
                r'26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:(?:0?[1-9])|(?:1[0-2]))(\/|-|\.)(?:0?[1-9]|1\d|2['
                r'0-8])\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$',
        'time': r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$',
    }


settings = Settings()

input_data: dict = {}
