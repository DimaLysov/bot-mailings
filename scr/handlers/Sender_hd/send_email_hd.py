from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from create_bot import bot
from utils.create_info_for_sending_emails import create_info

send_email_router = Router()


class FormSendEmail(StatesGroup):
    emails = State()


@send_email_router.message(Command('send_email'))
async def accept_emails(m: Message, state: FSMContext):
    await state.set_state(FormSendEmail.emails)
    await m.answer(text='Введите список почт, на которое нужно отправлять письма')


@send_email_router.message(FormSendEmail.emails)
async def cmd_send_emails(m: Message, state: FSMContext):
    emails = [email.strip() for email in m.text.split('\n')]
    info_sending = await create_info(m.from_user.id, emails)
    await m.answer(text='Подождите, письма отправляются')
    info_sending.send_email()
    await bot.edit_message_text(text='Письма отправлены!', chat_id=m.chat.id, message_id=m.message_id + 1)
    await m.answer(text='Все получилось')
    await state.clear()
