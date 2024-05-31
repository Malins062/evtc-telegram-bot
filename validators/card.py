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
