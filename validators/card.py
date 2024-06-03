import re

from pydantic import ValidationError

from config_data.config import settings


def validate_gn(text: str) -> str | None:
    try:
        gn = text.upper()
        gn = ''.join(re.findall(r'[0-9A-ZА-Я]+', gn))
        if not gn or not (2 <= len(gn) <= 9):
            raise ValidationError
    except ValidationError:
        return None

    return gn


def validate_article(text: str) -> str | None:
    try:
        article = text.upper()
        if not article or not (2 <= len(article) <= 300):
            raise ValidationError
    except ValidationError:
        return None

    return article


def validate_parking(text: str) -> str | None:
    try:
        parking = text.upper()
        if not parking or not (2 <= len(parking) <= 100):
            raise ValidationError
    except ValidationError:
        return None

    return parking


def validate_address(text: str) -> str | None:
    try:
        address = text.upper()
        if not address or not (2 <= len(address) <= 100):
            raise ValidationError
    except ValidationError:
        return None

    return address


def validate_protocol(text: str) -> str | None:
    try:
        # protocol = text.upper()
        protocol = ''.join(re.findall(r'[0-9]+', text))
        if not protocol or not len(protocol) == 6:
            raise ValidationError
        # protocol = ''.join(re.findall(r'[0-9А-Я]+', protocol))
        # if not (protocol and
        #         (len(protocol) == 10) and
        #         re.fullmatch(r'62[А-Я]{2}[0-9]{6}', protocol)):
        #     raise ValidationError
    except ValidationError:
        return None

    return protocol


def validate_model(text: str) -> str | None:
    try:
        model = text.upper()
        if not model or not (2 <= len(model) <= 25):
            raise ValidationError
    except ValidationError:
        return None

    return model


def validate_dt(text: str) -> str | None:
    try:
        digits = re.findall(r'(\d{2}).*(\d{2}).*(\d{4}).*(\d{2}).*(\d{2})', text)
        dt = ''
        if digits:
            date = '.'.join(digits[0][:3])
            time = ':'.join(digits[0][3:5])
            if (re.fullmatch(settings.patterns['date'], date)
                    and re.fullmatch(settings.patterns['time'], time)):
                dt = date + ' ' + time

        if not dt or not (len(dt) == 16):
            raise ValidationError
    except ValidationError:
        return None

    return dt
