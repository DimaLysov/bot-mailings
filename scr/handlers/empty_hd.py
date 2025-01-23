from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.InLine_kb.main_inline_kb import main_start_inline_kb

empty_router = Router()

@empty_router.message(Command('empty'))
async def cmd_empty(m: Message, state: FSMContext):
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())

