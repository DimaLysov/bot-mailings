from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def kb_all_sample_info():
    kb_list = [[KeyboardButton(text='Тема'), KeyboardButton(text='Текст'), KeyboardButton(text='Фото')]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return keyboard