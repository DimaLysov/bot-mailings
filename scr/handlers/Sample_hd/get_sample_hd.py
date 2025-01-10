import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from config import PHOTO_SAVE_PATH
from create_bot import bot
from db.requests.Samples.get_selected_sample_db import get_selected_sample

get_sample_router = Router()


@get_sample_router.message(Command('get_sample'))
async def cmd_get_sample(m: Message):
    sample = await get_selected_sample(m.from_user.id)
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
