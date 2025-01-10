from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from db.requests.Samples.get_all_themes_db import get_all_themes
from db.requests.Samples.update_status_sample_db import update_status_sample
from keyboards.select_sample_kb import kb_select_sample

select_sample_router = Router()


class FormSelectSample(StatesGroup):
    sample = State()


@select_sample_router.message(Command('select_sample'))
async def accept_sample(m: Message, state: FSMContext):
    await state.set_state(FormSelectSample.sample)
    themes_samples = await get_all_themes(m.from_user.id)
    if themes_samples is None:
        await m.answer(text='У вас нет ни одного шаблона')
    else:
        await m.answer(text='Выберете тему шаблона, который хотите выбрать',
                       reply_markup=kb_select_sample(themes_samples))


@select_sample_router.message(FormSelectSample.sample)
async def cmd_select_sample(m: Message, state: FSMContext):
    await update_status_sample(m.from_user.id, m.text)
    await m.answer(text='Вы успешно сменили тему', reply_markup=ReplyKeyboardRemove())
    await state.clear()
