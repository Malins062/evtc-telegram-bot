import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
    )

    bot_token: str = os.getenv('BOT_TOKEN')
    prefix: str = '!/\\'

    select_values: dict = {
        'model': ['ВАЗ', 'КИА', 'МЕРСЕДЕС', 'ТОЙОТА', 'ЛЕКСУС', 'БМВ', 'GEELY', 'HAVAL'],
        'gn': ['БН'],
        'protocol': ['АВ', 'ПЗ'],
    }


settings = Settings()
