import asyncio
from typing import Dict, Any

from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.context import FSMContext
from magic_filter import F
from aiogram import Router, types
from sqlalchemy.ext.asyncio import AsyncSession

from FSM_states.states import AdminForm
from db.db_requests import add_user, del_user
from keyboards.admin_kb import get_admin_kb_reply, admin_confirm_kb

router = Router()
router.message.filter(F.chat.id == 630887185)




@router.message(Command(commands=["admin"]))
async def cmd_admin(message: types.Message, state: FSMContext):
    await state.set_state(AdminForm.choosing)
    await message.answer("Выберите действие:", reply_markup=get_admin_kb_reply())


@router.message(F.text == "Отменить")
async def cancel_admin_cmd(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Отмена, для админки введи: /admin, для начала работы: /start",
                         reply_markup=types.ReplyKeyboardRemove())


@router.message(AdminForm.choosing, F.text == "Добавить в БД")
async def chose_add(message: types.Message, state: FSMContext):
    await state.set_state(AdminForm.add)
    await message.answer("Введите Telegram ID и Username пользователя,"
                         " которого Вы хотите добавить (прим.: 12345869,Revinder2)")


@router.message(AdminForm.choosing, F.text == "Удалить из БД")
async def chose_del(message: types.Message, state: FSMContext):
    await state.set_state(AdminForm.delete)
    await message.answer("Введите Telegram ID пользователя"
                         " которого Вы хотите удалить (прим.: 12345869234)")


@router.message(AdminForm.add)
async def add_user_to_db(message: types.Message, state: FSMContext):
    try:
        user_id = message.text.split(',')[0]
        username = message.text.split(',')[1]
        data = await state.update_data(user_id=user_id, username=username)
        await admin_show_summary(data=data, message=message)
        await state.set_state(AdminForm.confirmed_add)
        await state.update_data(user_id=user_id, username=username)
    except IndexError:
        await message.answer("Неверный формат (id,username)")


@router.message(AdminForm.delete)
async def del_user_from_db(message: types.Message, state: FSMContext):
    try:
        user_id = message.text.split(',')[0]
        data = await state.update_data(user_id=user_id)
        await admin_show_summary(data=data, message=message)
        await state.set_state(AdminForm.confirmed_delete)
        await state.update_data(user_id=user_id)
    except IndexError:
        await message.answer("Неверный формат (id)")


async def admin_show_summary(data: Dict[str, Any], message: types.Message):
    user_id = data["user_id"]
    username = data.get("username")
    if username:
        text = f"Telegram ID пользователя: {user_id}\nUsername пользователя: {username}"
    else:
        text = f"Telegram ID пользователя: {user_id}"
    await message.answer(text=text)
    await message.answer(text="Всё верно?", reply_markup=admin_confirm_kb())


@router.message(AdminForm.confirmed_add, F.text == "Подтвердить")
async def confirm_add(message: types.Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    user_id = data["user_id"]
    username = data["username"]
    if await add_user(session, int(user_id), username):
        await state.clear()
        await message.answer("Пользователь успешно добавлен!", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Пользователь с таким ID уже существует, начинай сначала: /admin",
                             reply_markup=types.ReplyKeyboardRemove())


@router.message(AdminForm.confirmed_delete, F.text == "Подтвердить")
async def confirm_del(message: types.Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    user_id = data["user_id"]
    if await del_user(session, int(user_id)):

        await state.clear()
        await message.answer("Пользователь успешно удален!", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Такого пользователя не существует", reply_markup=types.ReplyKeyboardRemove())







