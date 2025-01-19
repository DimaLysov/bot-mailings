from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def kb_select_email(emails):
    kb_list = []
    for item in range(1, len(emails), 2):
        kb_list.append([KeyboardButton(text=emails[item - 1]), KeyboardButton(text=emails[item])])
    if len(emails) % 2 != 0:
        kb_list.append([KeyboardButton(text=emails[-1])])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return keyboard
