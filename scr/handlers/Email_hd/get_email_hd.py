from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


from db.requests.Users_Emails.get_selected_email_db import get_selected_email

get_email_router = Router()


@get_email_router.message(Command('get_email'))
async def cmd_get_email(m: Message):
    email = await get_selected_email(m.from_user.id)
    if email is not None:
        await m.answer(text=f'Активная почта: {email}')
    else:
        await m.answer(text='У вас нет почт')
