from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class validate_username(validators.RegexValidator):
    regex = r"^[\w.@+-]+\Z"
    message = (
        "Введите корректное имя пользователя."
        "Это значение может содержать только буквы, цифры, "
        "и @/./+/-/_ символы."
    )
    flags = 0
