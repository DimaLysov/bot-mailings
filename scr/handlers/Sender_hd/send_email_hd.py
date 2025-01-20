from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from create_bot import bot
from db.requests.Samples.get_selected_sample_db import get_selected_sample
from db.requests.Users_Emails.get_selected_email_db import get_selected_email
from keyboards.InLine_kb.main_inline_kb import main_start_inline_kb
from utils.create_info_for_sending_emails import create_info

send_email_router = Router()


class FormSendEmail(StatesGroup):
    emails = State()


@send_email_router.callback_query(F.data == 'main_sender')
async def call_main_sender(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    answer_email = await get_selected_email(call.from_user.id)
    answer_sample = await get_selected_sample(call.from_user.id)
    if answer_email is None:
        await call.message.answer(text='Вы не можете отправлять письма, пока не добавите почту')
        await call.message.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
    elif answer_sample is None:
        await call.message.answer(text='Вы не можете отправлять письма, пока не добавите шаблон')
        await call.message.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
    else:
        await state.set_state(FormSendEmail.emails)
        await call.message.answer(text='Введите список почт, на которое нужно отправлять письма')


@send_email_router.message(FormSendEmail.emails)
async def cmd_send_emails(m: Message, state: FSMContext):
    emails = [email.strip() for email in m.text.split('\n')]
    info_sending = await create_info(m.from_user.id, emails)
    await m.answer(text='Подождите, письма отправляются')
    answer = info_sending.send_email()
    if not answer:
        await bot.edit_message_text(text='Все письма отправлены!', chat_id=m.chat.id, message_id=m.message_id + 1)
    else:
        info = ''
        for email in answer:
            info += f'{email}\n'
        await m.answer(text='Вот почты, на которые не получилось отправить письмо:\n' + info)
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
