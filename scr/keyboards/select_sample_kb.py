from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def kb_select_sample(themes):
    kb_list = []
    for item in range(1, len(themes), 2):
        kb_list.append([KeyboardButton(text=themes[item - 1]), KeyboardButton(text=themes[item])])
    if len(themes) % 2 != 0:
        kb_list.append([KeyboardButton(text=themes[-1])])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return keyboard
