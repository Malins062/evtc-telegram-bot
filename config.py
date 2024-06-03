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

        'article': {
            'ЗНАК 3.27':
                'ОСТАНОВКА ТС В ЗОНЕ ДЕЙСТВИЯ ЗНАКА 3.27 (П.П.1.3) СТ.12.16 Ч.4',
            'ПЕШЕХОДНЫЙ ПЕРЕХОД':
                'ОСТАНОВКА НА ПЕШЕХОДНОМ ПЕРЕХОДЕ ИЛИ БЛИЖЕ 5М ПЕРЕД НИМ (П.П.12.4) СТ.12.9 Ч.3',
            'ТРОТУАР 6.4':
                'ОСТАНОВКА ТС НА ТРОТУАРЕ ПРИ ОТСУТСТВИИ ЗНАКА 6.4 (П.П.12.2) СТ.12.9 Ч.3',
            'ИНВАЛИД 3.28':
                'СТОЯНКА ТС БЕЗ ТАБЛИЧКИ "ИНВАЛИД" В ЗОНЕ ДЕЙСТВИЯ ЗНАКА 3.28 СТ.12.16 Ч.4',
            'ИНВАЛИД 3.29':
                'СТОЯНКА ТС БЕЗ ТАБЛИЧКИ "ИНВАЛИД" В ЗОНЕ ДЕЙСТВИЯ ЗНАКА 3.29 СТ.12.16 Ч.4',
            'ИНВАЛИД 3.30':
                'СТОЯНКА ТС БЕЗ ТАБЛИЧКИ "ИНВАЛИД" В ЗОНЕ ДЕЙСТВИЯ ЗНАКА 3.30 СТ.12.16 Ч.4',
            'ИНВАЛИД 6.4':
                'СТОЯНКА ТС БЕЗ ТАБЛИЧКИ "ИНВАЛИД" В ЗОНЕ ДЕЙСТВИЯ ЗНАКА 6.4 (П.П.1.3) СТ.12.19 Ч.2',
            'ДАЛЕЕ 1-ГО РЯДА':
                'ОСТАНОВКА/СТОЯНКА ТС ДАЛЕЕ 1-ГО РЯДА КРАЯ ПРОЕЗЖЕЙ ЧАСТИ (П.П.12.2) СТ.12.19 Ч.2',
            'СОЗДАНИЕ ПОМЕХ':
                'ОСТАНОВКА/СТОЯНКА ТС, КОТОРОЕ ПОВЛЕКЛО СОЗДАНИЕ ПОМЕХ ДЛЯ ДРУГИХ ТС (П.П.12.4) СТ.12.19 Ч.3.2',
            'ООТ':
                'ОСТАНОВКА ТС, БЛИЖЕ 15М ОТ ООТ ЛИБО В МЕСТЕ ООТ (П.П.12.4) СТ.12.19 Ч.4',
        },

        'parking': {
            'СОЛНЕЧНАЯ': 'ООО КПФ ДИНАМО, ул.СОЛНЕЧНАЯ Д.1А, тел.8-930-783-33-02',
            'ОКСКИЙ ПР-Д': 'ИП Платонов, ОКСКИЙ ПРОЕЗД Д.15, тел.8-977-466-65-75, 40-70-74',
            'ТОВАРНЫЙ ДВОР': 'ООО АвтоТрансСервис 62, ул.ТОВАРНЫЙ ДВОР Д.60, тел.8-920-955-44-44',
            'СЕМИНАРСКАЯ': 'МП МКЦ, ул.СЕМИНАРСКАЯ Д.49, тел.8-900-606-03-05',
            'КОСТЫЧЕВА': 'ООО СпецТрансМО, ул.КОСТЫЧЕВА Д.15Б СТР.4, тел.8-960-603-44-62',
            'ГОРЬКОГО': 'ООО СпецТрансМО, ул.ГОРЬКОГО Д.1 СТР.2, тел.8-960-603-44-62',
        },
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
