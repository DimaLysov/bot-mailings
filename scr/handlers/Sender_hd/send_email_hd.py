from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from create_bot import bot
from keyboards.InLine_kb.main_inline_kb import main_start_inline_kb
from utils.create_info_for_sending_emails import create_info

send_email_router = Router()


class FormSendEmail(StatesGroup):
    emails = State()


@send_email_router.callback_query(F.data == 'main_sender')
async def call_main_sender(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await state.set_state(FormSendEmail.emails)
    await call.message.answer(text='Введите список почт, на которое нужно отправлять письма')


@send_email_router.message(FormSendEmail.emails)
async def cmd_send_emails(m: Message, state: FSMContext):
    emails = [email.strip() for email in m.text.split('\n')]
    info_sending = await create_info(m.from_user.id, emails)
    await m.answer(text='Подождите, письма отправляются')
    info_sending.send_email()
    await bot.edit_message_text(text='Письма отправлены!', chat_id=m.chat.id, message_id=m.message_id + 1)
    await m.answer(text='Все получилось')
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
