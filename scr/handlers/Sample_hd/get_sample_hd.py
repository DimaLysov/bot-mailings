import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, CallbackQuery

from config import PHOTO_SAVE_PATH, TEXT_SAVE_PATH
from create_bot import bot
from db.requests.Samples.get_selected_sample_db import get_selected_sample
from keyboards.InLine_kb.main_inline_kb import main_start_inline_kb

get_sample_router = Router()


@get_sample_router.callback_query(F.data == 'view_sample_call')
async def call_view_sample(call: CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    sample = await get_selected_sample(call.from_user.id)
    if sample is not None:
        photo_path = os.path.join(PHOTO_SAVE_PATH, sample.photo_name)
        text_path = os.path.join(TEXT_SAVE_PATH, sample.text_name)
        with open(text_path, 'r', encoding='utf-8') as file:
            text = file.read()
            await call.message.answer(text=f'Тема письма:\n\n'
                                           f'{sample.theme}\n\n'
                                           f'Текс письма\n\n'
                                           f'{text}\n\n')
        await call.message.answer(text='Фотографии письма:')
        await bot.send_photo(chat_id=call.message.chat.id, photo=FSInputFile(path=photo_path))
    else:
        await call.message.answer(text='Такого шаблона нет')
    await call.message.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
