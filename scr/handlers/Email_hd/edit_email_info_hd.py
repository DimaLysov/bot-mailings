from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from create_bot import bot
from db.requests.Users_Emails.edit_email_data_db import edit_date
from db.requests.Users_Emails.get_all_emails_db import get_emails
from keyboards.InLine_kb.main_inline_kb import main_start_inline_kb
from keyboards.Line_kb.email_password_kb import kb_email_password
from keyboards.Line_kb.select_email_kb import kb_select_email
from utils.check_data import is_valid_data

edit_router = Router()


class FormEdit(StatesGroup):
    main_email = State()
    select = State()
    edit_data = State()


@edit_router.callback_query(F.data == 'edit_email_data')
async def call_edit(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    emails = await get_emails(call.from_user.id)
    await state.set_state(FormEdit.main_email)
    await call.message.answer(text='Выберете почту, у которой хотите изменить данные\n\n'
                                   'Для выхода из режима - /empty',
                              reply_markup=kb_select_email(emails))


@edit_router.message(FormEdit.main_email)
async def make_choice(m: Message, state: FSMContext):
    if m.text != '/empty':
        if is_valid_data('Почта', m.text):
            await state.update_data(main_email=m.text)
            await state.set_state(FormEdit.select)
            await m.answer(text='Выберете, что хотите изменить', reply_markup=kb_email_password())
        else:
            await state.set_state(FormEdit.main_email)
            await m.answer(text='Вы ввели некорректное название почты, попробуйте еще раз', )
    else:
        await state.clear()
        await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@edit_router.message(FormEdit.select)
async def accept_select(m: Message, state: FSMContext):
    if m.text != '/empty':
        if m.text == 'Почта' or m.text == 'Пароль':
            await state.update_data(select=m.text)
            await state.set_state(FormEdit.edit_data)
            if m.text == 'Почта':
                await m.answer(text='Введите новую почту', reply_markup=ReplyKeyboardRemove())
            elif m.text == 'Пароль':
                await m.answer(text='Введите новый пароль', reply_markup=ReplyKeyboardRemove())
        else:
            await state.set_state(FormEdit.select)
            await m.answer('Извините, но я не знаю что это, попробуйте еще')
    else:
        await state.clear()
        await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())



@edit_router.message(FormEdit.edit_data)
async def edit_email_or_password(m: Message, state: FSMContext):
    if m.text != '/empty':
        data = await state.get_data()
        main_email = data.get('main_email')
        select = data.get('select')
        new_value = m.text
        if is_valid_data(select, new_value):
            answer = await edit_date(m.from_user.id, main_email, new_value, select)
            if answer:
                await m.answer(text='Вы успешно изменили данные')
            else:
                await m.answer(text='Не удалось изменить данные')
            await state.clear()
            await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
        else:
            await state.set_state(FormEdit.edit_data)
            await m.answer(text='Вы ввели не корректные данные, попробуйте еще раз')
    else:
        await state.clear()
        await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())