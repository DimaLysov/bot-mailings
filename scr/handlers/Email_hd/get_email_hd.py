from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from create_bot import bot
from db.requests.Users_Emails.get_selected_email_db import get_selected_email
from keyboards.InLine_kb.main_inline_kb import main_start_inline_kb

get_email_router = Router()


@get_email_router.callback_query(F.data == 'view_email_call')
async def call_get_email(call: CallbackQuery):
    email = await get_selected_email(call.from_user.id)
    if email is not None:
        await call.message.answer(text=f'Активная почта: {email}')
    else:
        await call.message.answer(text='У вас нет почт')
