from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from create_bot import bot
from keyboards.InLine_kb.main_inline_kb import main_start_inline_kb

empty_router = Router()

@empty_router.message(Command('empty'))
async def cmd_empty(m: Message, state: FSMContext):
    await state.clear()
    await m.answer(text='Выход...', reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(m.from_user.id, m.message_id+1)
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())

