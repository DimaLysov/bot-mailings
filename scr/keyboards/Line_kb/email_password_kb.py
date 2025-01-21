from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def kb_email_password():
    kb_list = [[KeyboardButton(text='Почта'), KeyboardButton(text='Пароль')]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return keyboard