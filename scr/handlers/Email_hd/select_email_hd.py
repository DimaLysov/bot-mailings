from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from create_bot import bot
from db.requests.Users.get_user_id_db import get_user_id
from db.requests.Users_Emails.get_all_emails_db import get_emails
from db.requests.Users_Emails.update_status_email_db import update_status_email
from keyboards.InLine_kb.main_inline_kb import main_start_inline_kb
from keyboards.Line_kb.select_email_kb import kb_select_email
from utils.check_data import is_valid_email

select_email_router = Router()


class FormSelectEmail(StatesGroup):
    email = State()


@select_email_router.callback_query(F.data == 'select_email_call')
async def call_select_email(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await state.set_state(FormSelectEmail.email)
    emails = await get_emails(call.from_user.id)
    if not emails:
        await call.message.answer(text='У вас ни одной почты')
        await state.clear()
        await call.message.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
    else:
        await call.message.answer(text='Выберите почту, с которой хотите отправлять письма',
                                  reply_markup=kb_select_email(emails))


@select_email_router.message(FormSelectEmail.email)
async def cmd_select_email(m: Message, state: FSMContext):
    if is_valid_email(m.text):
        answer = await update_status_email(await get_user_id(m.from_user.id), m.text)
        if answer:
            await m.answer(text='Вы успешно сменили почту!', reply_markup=ReplyKeyboardRemove())
        else:
            await m.answer(text='Такой почты у вас нет')
        await state.clear()
        await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
    else:
        emails = await get_emails(m.from_user.id)
        await m.answer(text='Вы ввели некорректный email, попробуйте еще раз', reply_markup=kb_select_email(emails))
        await state.set_state(FormSelectEmail.email)
