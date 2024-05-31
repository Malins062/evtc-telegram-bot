import re

from pydantic import ValidationError


def validate_gn(text: str) -> str | None:
    try:
        gn = text.upper()
        gn = re.sub(r'\s+', '', gn)
        if not gn or not (2 <= len(gn) <= 9):
            raise ValidationError
    except ValidationError:
        return None

    return gn


def validate_protocol(text: str) -> str | None:
    try:
        protocol = text.upper()
        protocol = re.sub(r'\s+', '', protocol)
        if not protocol or not (len(protocol) == 10):
            raise ValidationError
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
        dt = text
        if not dt or not (len(dt) == 16):
            raise ValidationError
    except ValidationError:
        return None

    return dt
