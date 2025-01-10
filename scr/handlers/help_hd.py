from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

help_router = Router()


@help_router.message(Command('help'))
async def cmd_help(m: Message):
    await m.answer(text='Вот список команд, которые могут пригодиться:\n'
                        'Для работы с почтой:\n'
                        '/set_email - <b>добавить почту</b>\n'
                        '/get_email - <b>показать выбранную почту</b>\n'
                        '/select_email - <b>выбрать почту (если вы ввели несколько)</b>\n'
                        '\n'
                        'Для работы с шаблоном:\n'
                        '/set_sample - <b>добавить шаблон</b>\n'
                        '/get_sample - <b>показать выбранный шаблон</b>\n'
                        '/select_sample - <b>выбрать шаблон (если вы создали несколько)</b>')

