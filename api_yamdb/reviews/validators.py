import re

from django.core.exceptions import ValidationError


REGEX_FOR_USERNAME = re.compile(r'^[\w.@+-]+')


def validate_username(name):
    if name == 'me':
        raise ValidationError('Имя пользователя "me" использовать запрещено!')
    if not REGEX_FOR_USERNAME.fullmatch(name):
        raise ValidationError(
            'Можно использовать только буквы, цифры и символы @.+-_".')
