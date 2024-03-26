import re

from django.core.exceptions import ValidationError


def validate_custom_number(value):
    if not re.match(r'^[1-9]\d{3}[A-Z]$', value):
        raise ValidationError(
            'Неверный формат. Формат должен быть: Цифра от 1000 до 9999 + заглавная буква английского '
            'алфавита в конце.')
