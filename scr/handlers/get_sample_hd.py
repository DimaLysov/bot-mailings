import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from config import PHOTO_SAVE_PATH
from create_bot import bot
from db.requests.Samples.get_sample_db import get_sample

get_sample_router = Router()


class FormGetSample(StatesGroup):
    them = State()


@get_sample_router.message(Command('get_sample'))
async def accept_them(m: Message, state: FSMContext):
    await state.set_state(FormGetSample.them)
    await m.answer(text='Введите тему от шаблона')


@get_sample_router.message(FormGetSample.them)
async def cmd_get_sample(m: Message, state: FSMContext):
    sample = await get_sample(m.from_user.id, m.text)
    if sample is not None:
        photo_path = os.path.join(PHOTO_SAVE_PATH, sample.photo)
        await m.answer(text=f'Тема письма:\n\n'
                            f'{sample.them}\n\n'
                            f'Текс письма\n\n'
                            f'{sample.text}\n\n')
        await m.answer(text='Фотографии письма:')
        await bot.send_photo(chat_id=m.chat.id, photo=FSInputFile(path=photo_path))
    else:
        await m.answer(text='Такого шаблона нет')
    await state.clear()
