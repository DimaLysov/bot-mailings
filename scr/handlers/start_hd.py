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
                            'Вижу что ты тут в первый раз😉\n\n'
                            'Этот бот поможет тебе создавать шаблоны, а после по ним отправлять письма с твоей gmail почты\n\n'
                            'Чтобы посмотреть полный функционал бота и как создавать пароль, нажми кнопку инструкция⬇️')
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
    await call.message.answer(text='<b>---------------------Инструкция по использованию---------------------</b>\n\n'
                                   'В боте существует всего 2 команды:\n\n'
                                   '/start - вызов панели навигации\n\n'
                                   '/empty - выход из любого режима (например изменения шаблона)\n\n'
                                   'Все остальное управление происходи через панель навигации\n\n'
                                   '<b>-------------------------Информация о данных-------------------------</b>\n\n'
                                   '<b>1️⃣Регистрация почты</b>\n\n'
                                   'Для того чтобы бот мог успешно отправлять письма с вашей gmail почты ему необходимо сообщить пароль от приложений\n'
                                   'Как его создать:\n'
                                   '1) Открыть "Управление аккаунтом в Google"\n\n'
                                   '2) Перейти во вкладку "Безопасность"\n\n'
                                   '3) Настроить двухэтапной аутентификация (Если она у вас не настроена).\n\n'
                                   '4) В поиске написать и открыть "пароли приложений".\n\n'
                                   '5) Называете ваше приложение и получаете пароль.\n\n'
                                   '6) Данный пароль и почту, с которой вы будите отсылать письма, используйте для создания почты в боте\n\n'
                                   '<b>2️⃣Создание шаблона</b>\n\n'
                                   'В данной версии бота шаблон создается по правилам:\n\n'
                                   '1) Сначала вводите тема и текст письма\n\n'
                                   '2) Далее прикрепляете необходимое количество фотографий\n\n'
                                   '<i>(Фотографии нужно присылать по одной, для правильной работы бота)</i>\n\n'
                                   '<b>3️⃣Отправка писем</b>\n\n'
                                   'Чтобы отправить письма, необходимо будет отправить список почт, написанных через enter.\n'
                                   'Бот проверит каждую почту на корректность написания и вернет не корректные почты\n\n')
    await call.message.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
