from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from create_bot import bot
from db.requests.Samples.get_all_themes_db import get_all_themes
from db.requests.Samples.update_status_sample_db import update_status_sample
from keyboards.InLine_kb.main_inline_kb import main_start_inline_kb
from keyboards.Line_kb.select_sample_kb import kb_select_sample

select_sample_router = Router()


class FormSelectSample(StatesGroup):
    sample = State()


@select_sample_router.callback_query(F.data == 'select_sample_call')
async def call_select_sample(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await state.set_state(FormSelectSample.sample)
    themes_samples = await get_all_themes(call.from_user.id)
    if themes_samples is None:
        await call.message.answer(text='У вас нет ни одного шаблона')
    else:
        await call.message.answer(text='Выберете тему шаблона, который хотите выбрать',
                                  reply_markup=kb_select_sample(themes_samples))


@select_sample_router.message(FormSelectSample.sample)
async def cmd_select_sample(m: Message, state: FSMContext):
    await update_status_sample(m.from_user.id, m.text)
    await m.answer(text='Вы успешно сменили тему', reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
