from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from db.requests.Users.user_registration_db import registration

start_router = Router()


@start_router.message(Command('start'))
async def cmd_start(m: Message):
    answer = await registration(m.from_user.id)
    if answer:
        await m.answer(text='Привет👋\n\n'
                            'Этот бот поможет тебе делать рассылки. Для начала давай создадим подключение\n\n'
                            'Введи команду /set_email')
    else:
        await m.answer(text='Привет👋\n'
                            'Ты уже пользовался данным ботом')
