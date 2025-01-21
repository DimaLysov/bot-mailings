from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from create_bot import bot
from db.requests.Users.user_registration_db import registration
from keyboards.InLine_kb.main_inline_kb import main_start_inline_kb, main_email_inline_kb, main_sample_inline_kb

start_router = Router()


@start_router.message(Command('start'))
async def cmd_start(m: Message):
    answer = await registration(m.from_user.id, m.from_user.username)
    if answer:
        await m.answer(text='Привет👋\n\n'
                            'Вижу что ты тут в первый раз.\n'
                            'Этот бот поможет тебе создавать шаблоны, а после по ним отправлять письма с твоей gmail почты\n\n'
                            'Примечание:\n\n'
                            'Данная версия бота позволяет создавать шаблон строго такого типа:\n'
                            '<b>тема письма</b> -> <b>основной текст</b> -> <b>фотография</b>\n\n'
                            'В будущем будем расширять функционал')
        await m.answer(text='Вот удобная панель для навигации')
        await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
    else:
        await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@start_router.callback_query(F.data == 'main_email')
async def write_main_email(call: CallbackQuery):
    await call.message.edit_reply_markup(str(call.message.message_id), reply_markup=main_email_inline_kb())


@start_router.callback_query(F.data == 'main_sample')
async def write_main_sample(call: CallbackQuery):
    await call.message.edit_reply_markup(str(call.message.message_id), reply_markup=main_sample_inline_kb())

@start_router.callback_query(F.data == 'back_main')
async def write_main_kb(call: CallbackQuery):
    await call.message.edit_reply_markup(str(call.message.message_id), reply_markup=main_start_inline_kb())

@start_router.callback_query(F.data == 'main_setting')
async def write_main_setting(call: CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer(text='Полная инструкция')
    await call.message.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
