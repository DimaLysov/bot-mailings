import re


def is_valid_data(object_check, value):
    if object_check == 'Почта':
        return is_valid_email(value)
    elif object_check == 'Пароль':
        return is_valid_password(value)


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_valid_password(sentence):
    return len(sentence) == 16
