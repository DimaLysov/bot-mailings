import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from config import PHOTO_SAVE_PATH
from create_bot import bot
from db.requests.Samples.add_sample_db import add_sample

add_sample_router = Router()


class FormSample(StatesGroup):
    theme = State()
    text = State()
    photo = State()


@add_sample_router.message(Command('set_sample'))
async def accept_them(m: Message, state: FSMContext):
    await state.set_state(FormSample.theme)
    await m.answer(text='Введите тему для вашего письма')


@add_sample_router.message(FormSample.theme)
async def accept_text(m: Message, state: FSMContext):
    await state.update_data(theme=m.text)
    await state.set_state(FormSample.text)
    await m.answer(text='Введите текс который будет в письме')


@add_sample_router.message(FormSample.text)
async def accept_photo(m: Message, state: FSMContext):
    await state.update_data(text=m.text)
    await state.set_state(FormSample.photo)
    await m.answer(text='Отправьте фотографию, которая будет в письме')


@add_sample_router.message(FormSample.photo)
async def set_sample(m: Message, state: FSMContext):
    photo_id = m.photo[-1].file_id
    print(photo_id)
    photo = await bot.get_file(photo_id)
    photo_name = f"{photo_id}.jpg"
    await bot.download_file(photo.file_path, os.path.join(PHOTO_SAVE_PATH, photo_name))

    date = await state.get_data()
    theme = date.get('theme')
    text = date.get('text')
    answer = await add_sample(m.from_user.id, theme, text, photo_name)
    if answer:
        await m.answer(text='Вы успешно сохранили шаблон письма')
    else:
        await m.answer(text='Что-то пошло не так...')
    await state.clear()
