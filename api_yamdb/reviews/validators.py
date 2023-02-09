import datetime as datetime
import re

from django.core.exceptions import ValidationError


REGEX_FOR_USERNAME = re.compile(r'^[\w.@+-]+')

MAX_VALUE_COMMENT = 5000


def validate_username(name):
    """Проверка поля username на соответствие требованиям."""
    if name == 'me':
        raise ValidationError('Имя пользователя "me" использовать запрещено!')
    if not REGEX_FOR_USERNAME.fullmatch(name):
        raise ValidationError(
            'Можно использовать только буквы, цифры и символы @.+-_".')


def year_validator(value):
    """Проверка значения года - не больше существующего."""
    if value > datetime.datetime.now().year:
        raise ValidationError(
            f"год {value} не может быть больше текущего",
            params={"value": value},
        )


def max_length_validator(value):
    """Проверка макс длины комментария."""
    if len(value) > MAX_VALUE_COMMENT:
        raise ValidationError(
            f'Длина комментария {value}'
            f'не может быть больше {MAX_VALUE_COMMENT}',
            params={"value": value},
        )
