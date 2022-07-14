import asyncio
from typing import Dict, Any
from aiogram.dispatcher.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from magic_filter import F
from FSM_states.states import CategoryForm
from aiogram import Router, types
from keyboards.discount_kb_factory import DiscountCallbackFactory, get_discount_kb_fab
from keyboards.wb_keyboard import CategoryCallbackFactory, get_keyboard_fab, confirm_category_kb

router = Router()
# router.message.filter(F.chat.type.in_({"private", }))


@router.message(commands=["start"])
async def cmd_start_fab(message: types.Message, state: FSMContext):
    await state.set_state(CategoryForm.category)
    await message.answer("Привет! Я бот, который будет следить за реальными снижениями цен на товары в Wildberries!")
    await message.answer("Выберите категорию: ", reply_markup=get_keyboard_fab())


@router.callback_query(DiscountCallbackFactory.filter(F.action == "stop"))
@router.callback_query(CategoryCallbackFactory.filter(F.action == "stop"))
async def callback_cmd_cancel(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await callback.message.answer(f"Отмена. Для выбора категории введите /start")
    await asyncio.sleep(1)
    await callback.message.delete()
    await callback.answer()


@router.message(F.text.casefold() == 'отмена')
async def msg_cmd_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(f"Отмена. Для выбора категории введите /start")
    await asyncio.sleep(1)
    await message.delete()


@router.callback_query(CategoryForm.category, CategoryCallbackFactory.filter())
async def get_sundresses(callback: types.CallbackQuery, state: FSMContext, callback_data: CategoryCallbackFactory):
    await state.update_data(category=callback_data.name)
    await state.set_state(CategoryForm.size)
    await callback.message.answer(f"Вы выбрали категорию {callback_data.name}\nТеперь введите свой размер (40, 41, "
                                  f"42 и т.д...). Или напишите 'Отмена' для того чтобы начать заново")
    print(callback)
    print(callback.from_user.id, callback.from_user.first_name)
    await asyncio.sleep(1)
    await callback.message.delete()
    await callback.answer()


@router.message(CategoryForm.size)
async def get_size(message: types.Message, state: FSMContext):
    try:
        int(message.text)
    except ValueError:
        await message.reply("Введите размер")
    await state.update_data(size=message.text)
    print(message)
    await state.set_state(CategoryForm.discount)
    await message.answer(f"Теперь выберите размер скидки", reply_markup=get_discount_kb_fab())



@router.callback_query(CategoryForm.discount, DiscountCallbackFactory.filter())
async def get_discount(callback: types.CallbackQuery, state: FSMContext, callback_data: DiscountCallbackFactory):
    data = await state.update_data(discount=callback_data.discount)
    await show_summary(data=data, callback=callback)
    # await state.clear()
    await state.set_state(CategoryForm.confirmed)
    await asyncio.sleep(1)
    await callback.message.delete()
    await callback.answer()


async def show_summary(data: Dict[str, Any], callback: types.CallbackQuery = None):
    category = data["category"]
    size = data.get("size", "something_unexpected")
    discount = data.get("discount", "something_unexpected")
    text = f'Ваша категория: {category}\nРазмер: {size}\nСкидка: {discount}'
    await callback.message.answer(text=text)
    await callback.message.answer(text="Всё верно?", reply_markup=confirm_category_kb())



@router.callback_query(CategoryForm.confirmed, CategoryCallbackFactory.filter(F.name == "confirm"))
async def confirmed_category(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Спасибо!")
    await asyncio.sleep(1)
    await callback.message.delete()
    await callback.answer()
    # return True

