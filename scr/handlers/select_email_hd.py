from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from db.requests.Users.get_user_id_db import get_user_id
from db.requests.Users_Emails.get_all_emails_db import get_emails
from db.requests.Users_Emails.update_status_email_db import update_status_email
from keyboards.select_email_kb import kb_select_email

select_email_router = Router()


class FormSelectEmail(StatesGroup):
    email = State()


@select_email_router.message(Command('select_email'))
async def accept_email(m: Message, state: FSMContext):
    await state.set_state(FormSelectEmail.email)
    emails = await get_emails(m.from_user.id)
    if emails is None:
        await m.answer(text='У вас ни одной почты')
    else:
        await m.answer(text='Выберите почту, с которой хотите отправлять письма', reply_markup=kb_select_email(emails))


@select_email_router.message(FormSelectEmail.email)
async def cmd_select_email(m: Message, state: FSMContext):
    await update_status_email(await get_user_id(m.from_user.id), m.text)
    await m.answer(text='Вы успешно сменили почту!', reply_markup=ReplyKeyboardRemove())
    await state.clear()
