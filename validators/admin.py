import re

from pydantic import ValidationError


def validate_phone_number(text: str) -> str | None:
    try:
        phone_number = ''.join(re.findall(r'[0-9,\\+]+', text))
        if not (phone_number and
                re.fullmatch(r'^\+[1-9][0-9]{7,14}$', phone_number)):
            raise ValidationError
    except ValidationError:
        return None

    return phone_number
