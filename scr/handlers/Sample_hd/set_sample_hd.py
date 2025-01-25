import os
import time

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from config import PHOTO_SAVE_PATH, TEXT_SAVE_PATH
from create_bot import bot
from db.requests.Photos.add_photo_db import add_new_photo
from db.requests.Photos.get_all_photos_sample_db import get_all_photos
from db.requests.Samples.add_sample_db import add_sample
from keyboards.InLine_kb.main_inline_kb import main_start_inline_kb

add_sample_router = Router()


class FormSample(StatesGroup):
    theme = State()
    text = State()
    count_photos = State()
    photo = State()


@add_sample_router.callback_query(F.data == 'new_sample_call')
async def call_new_sample(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await state.set_state(FormSample.theme)
    await call.message.answer(text='Введите тему для вашего письма\n\n'
                                   'Для выхода из режима - /empty')


@add_sample_router.message(FormSample.theme)
async def accept_text(m: Message, state: FSMContext):
    if m.text == '/empty':
        await state.clear()
        await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
    else:
        await state.update_data(theme=m.text)
        await state.set_state(FormSample.text)
        await m.answer(text='Введите текс который будет в письме')


@add_sample_router.message(FormSample.text)
async def add_text(m: Message, state: FSMContext):
    if m.text == '/empty':
        await state.clear()
        await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
    else:
        await state.update_data(text=m.text)
        date = await state.get_data()
        # Сохраняем текст
        text = date.get('text')
        text_name = f"file_{m.from_user.id}_{int(time.time())}.txt"
        text_file_path = os.path.join(TEXT_SAVE_PATH, text_name)
        with open(text_file_path, 'a', encoding='utf-8') as file:
            file.write(text)
        # Добавляем шаблон в бд
        theme = date.get('theme')
        answer = await add_sample(m.from_user.id, theme, text_name)
        if answer:
            await m.answer(text='Текст письма сохранен')
            await m.answer(text='Введите количество фотографий, которые будут в шаблоне\n\n'
                                '(Если фотографий не будет, введите 0)')
            await state.set_state(FormSample.count_photos)
        else:
            await m.answer(text='Не удалось сохранить текст')
            await state.clear()
            await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@add_sample_router.message(FormSample.count_photos)
async def accept_count_photo(m: Message, state: FSMContext):
    if m.text != '/empty':
        if m.text.isdigit():
            count = int(m.text)
            if count != 0:
                await state.update_data(count_photo=count)
                await m.answer(text='Для лучшей работы бота, не группируйте фотографии')
                await state.set_state(FormSample.photo)
                return
        else:
            await m.answer(text='Вы ввели некорректное число, попробуйте еще раз')
            await state.set_state(FormSample.count_photos)
            return
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@add_sample_router.message(FormSample.photo)
async def accept_photo(m: Message, state: FSMContext):
    if m.text != '/empty':
        date = await state.get_data()
        all_count = date.get('count_photo')
        # Сохраняем фотографию
        photo_id = m.photo[-1].file_id
        photo = await bot.get_file(photo_id)
        photo_name = f"{photo_id}.jpg"
        await bot.download_file(photo.file_path, os.path.join(PHOTO_SAVE_PATH, photo_name))
        # Добавляем названия фотографии в бд
        theme = date.get('theme')
        answer = await add_new_photo(theme, photo_name)
        if answer:
            await m.answer(text='Фотография сохранена')
        else:
            await m.answer(text='Произошла ошибка')
        count_photo = len(await get_all_photos(theme))
        if all_count > count_photo:
            await state.set_state(FormSample.photo)
            return
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
