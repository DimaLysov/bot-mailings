import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.util import await_only

from config import TEXT_SAVE_PATH, PHOTO_SAVE_PATH
from create_bot import bot
from db.requests.Photos.add_photo_db import add_new_photo
from db.requests.Photos.delete_photos_db import delete_photo
from db.requests.Photos.get_all_photos_sample_db import get_all_photos
from db.requests.Samples.edit_them_sample_db import edit_theme_sample
from db.requests.Samples.get_all_themes_db import get_all_themes
from db.requests.Samples.get_sample_text_db import get_name_text
from keyboards.InLine_kb.main_inline_kb import main_start_inline_kb
from keyboards.Line_kb.all_sample_info_kb import kb_all_sample_info
from keyboards.Line_kb.select_sample_kb import kb_select_sample

edit_sample_router = Router()


class FormEditSample(StatesGroup):
    main_sample = State()
    select_user = State()
    edit_theme = State()
    edit_text = State()
    count_photo = State()
    edit_photo = State()


@edit_sample_router.callback_query(F.data == 'edit_sample_data')
async def call_edit_sample(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    themes = await get_all_themes(call.from_user.id)
    if not themes:
        await call.message.answer(text='У вас нет ни одного шаблона')
        await call.message.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
    else:
        await call.message.answer(text='Выберете, шаблон, который хотите изменить\n\n'
                                       'Для выхода из режима /empty', reply_markup=kb_select_sample(themes))
        await state.set_state(FormEditSample.main_sample)


@edit_sample_router.message(FormEditSample.main_sample)
async def accept_main_sample(m: Message, state: FSMContext):
    await state.update_data(main_sample=m.text)
    await m.answer(text='Выберете, что хотите изменить', reply_markup=kb_all_sample_info())
    await state.set_state(FormEditSample.select_user)


@edit_sample_router.message(FormEditSample.select_user)
async def accept_select_user(m: Message, state: FSMContext):
    if m.text == 'Тема':
        await state.update_data(select_user=m.text)
        await m.answer(text='Введите новую тему', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FormEditSample.edit_theme)
    elif m.text == 'Текст':
        await state.update_data(select_user=m.text)
        await m.answer(text='Введите новый текст', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FormEditSample.edit_text)
    elif m.text == 'Фото':
        await state.update_data(select_user=m.text)
        await m.answer(text='Введите количество фотографий, которые будут в шаблоне\n\n'
                            '(Если фотографий не будет, введите 0)', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FormEditSample.count_photo)


@edit_sample_router.message(FormEditSample.edit_theme)
async def accept_new_theme(m: Message, state: FSMContext):
    data = await state.get_data()
    main_sample = data.get('main_sample')
    answer = await edit_theme_sample(m.from_user.id, main_sample, m.text)
    if answer:
        await m.answer(text='Вы успешно изменили тему')
    else:
        await m.answer(text='Не удалось изменить')
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@edit_sample_router.message(FormEditSample.edit_text)
async def accept_new_text(m: Message, state: FSMContext):
    data = await state.get_data()
    main_sample = data.get('main_sample')
    text_name = await get_name_text(m.from_user.id, main_sample)
    file_path = os.path.join(TEXT_SAVE_PATH, text_name)
    os.remove(file_path)
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(m.text)
    await m.answer(text='Вы успешно изменили текст письма')
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@edit_sample_router.message(FormEditSample.count_photo)
async def accept_count_photo(m: Message, state: FSMContext):
    data = await state.get_data()
    main_sample = data.get('main_sample')
    photos_names = await get_all_photos(main_sample)
    # удаляем фотографии из бд
    answer = await delete_photo(main_sample)
    if answer:
        # удаляем фотографии из папки
        for photo in photos_names:
            file_path = os.path.join(PHOTO_SAVE_PATH, photo)
            os.remove(file_path)
        if m.text.isdigit():
            count = int(m.text)
            if count != 0:
                await state.update_data(count_photo=count)
                await m.answer(text='Для лучшей работы бота, не группируйте фотографии')
                await state.set_state(FormEditSample.edit_photo)
            else:
                await state.clear()
                await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
        else:
            await m.answer(text='Вы ввели некорректное число, попробуйте еще раз')
            await state.set_state(FormEditSample.count_photo)
    else:
        await m.answer(text='Произошла ошибка при удаление')
        await state.clear()
        await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@edit_sample_router.message(FormEditSample.edit_photo)
async def accept_photos(m: Message, state: FSMContext):
    date = await state.get_data()
    all_count = date.get('count_photo')
    # Сохраняем фотографию
    photo_id = m.photo[-1].file_id
    photo = await bot.get_file(photo_id)
    photo_name = f"{photo_id}.jpg"
    await bot.download_file(photo.file_path, os.path.join(PHOTO_SAVE_PATH, photo_name))
    # Добавляем названия фотографии в бд
    main_sample = date.get('main_sample')
    answer = await add_new_photo(main_sample, photo_name)
    if answer:
        await m.answer(text='Фотография сохранена')
    else:
        await m.answer(text='Произошла ошибка')
    count_photo = len(await get_all_photos(main_sample))
    if all_count > count_photo:
        await state.set_state(FormEditSample.edit_photo)
        return
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
