from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

help_router = Router()


@help_router.message(Command('help'))
async def cmd_help(m: Message):
    await m.answer(text='Вот список команд, которые могут пригодиться:\n'
                        '/start\n'
                        '/set_email\n'
                        '/set_sample\n'
                        '/get_sample')

