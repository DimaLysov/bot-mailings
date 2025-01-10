from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

help_router = Router()


@help_router.message(Command('help'))
async def cmd_help(m: Message):
    await m.answer(text='Вот список команд, которые могут пригодиться:\n'
                        '/set_email - добавить почту\n'
                        '/set_sample - добавить шаблон\n'
                        '/get_sample - показать выбранный шаблон\n'
                        '/get_email - показать выбранную почту\n'
                        '/select_email - выбрать почту (если вы ввели несколько)\n'
                        '/select_sample - выбрать шаблон (если вы создали несколько)')

