from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_start_inline_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text='Мои почты 📤', callback_data='main_email'),
         InlineKeyboardButton(text='Мои шаблоны 📝', callback_data='main_sample')],
        [InlineKeyboardButton(text='Отправлять письма 📩', callback_data='main_sender'),
         InlineKeyboardButton(text='Инструкция ⚙️', callback_data='main_setting')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def main_email_inline_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text='Новая почту 🆕', callback_data='new_email_call'),
         InlineKeyboardButton(text='Показать выбранную 👀', callback_data='view_email_call')],
        [InlineKeyboardButton(text='Выбрать почту 🫵', callback_data='select_email_call'),
         InlineKeyboardButton(text='Изменить данные ✍️', callback_data='edit_email_data')],
         [InlineKeyboardButton(text='В главное меню ⬅️', callback_data='back_main')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def main_sample_inline_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text='Новый шаблон 🆕', callback_data='new_sample_call'),
         InlineKeyboardButton(text='Показать выбранный 👀', callback_data='view_sample_call')],
        [InlineKeyboardButton(text='Выбрать шаблон 🫵', callback_data='select_sample_call'),
         InlineKeyboardButton(text='Изменить шаблон ✍️', callback_data='edit_sample_data')],
        [InlineKeyboardButton(text='В главное меню ⬅️', callback_data='back_main')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
