from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from create_bot import bot
from keyboards.InLine_kb.main_inline_kb import main_start_inline_kb
from utils.check_email import is_valid_email
from utils.check_password import is_valid_password
from db.requests.Users_Emails.add_email_db import add_email

add_email_router = Router()


class FormEditConn(StatesGroup):
    user_email = State()
    user_email_pass = State()


@add_email_router.callback_query(F.data == 'new_email_call')
async def call_set_email(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('Введите название почты, с которой вы хотите отправлять письма\n\n'
                              'Пример: ivanivanov@mail.ru')
    await state.set_state(FormEditConn.user_email)


@add_email_router.message(FormEditConn.user_email)
async def accept_pass(m: Message, state: FSMContext):
    await state.update_data(user_email=m.text)
    user_data = await state.get_data()
    email = user_data.get('user_email')
    if is_valid_email(email):
        await m.answer('Введите пароль для приложений\n\n'
                       'Как создать пароль можно посмотреть здесь - https://github.com/DimaLysov/Mailings-by-mail/blob/master/README.md#подключение\n\n'
                       'Пример: yima fekd rylw weux')
        await state.set_state(FormEditConn.user_email_pass)
    else:
        await m.answer(text='Вы ввели неккоректный email, попробуйте еще раз')
        await state.set_state(FormEditConn.user_email)


@add_email_router.message(FormEditConn.user_email_pass)
async def cmd_get_email(m: Message, state: FSMContext):
    await state.update_data(user_email_pass=m.text)
    user_data = await state.get_data()
    email = user_data.get('user_email')
    password = user_data.get('user_email_pass')
    print(email, password)
    if is_valid_password(password):
        answer = await add_email(email, password, m.from_user.id)
        if answer:
            await m.answer(text='Вы успешно ввели данные')
        else:
            await m.answer(text='Произошла какая-то ошибка')
        await state.clear()
    else:
        await m.answer(text='Вы ввели некорректный пароль, попробуйте еще раз')
        await state.set_state(FormEditConn.user_email_pass)
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
