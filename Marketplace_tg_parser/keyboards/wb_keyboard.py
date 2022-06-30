from aiogram import types
from typing import Optional
from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class CategoryCallbackFactory(CallbackData, prefix="main_cat"):
    name: str
    action: Optional[str]


def get_keyboard_fab():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Сарафаны", callback_data=CategoryCallbackFactory(name="Сарафаны")
    )
    builder.button(
        text="Платья", callback_data=CategoryCallbackFactory(name="Платья")
    )
    builder.button(
        text="Все вместе", callback_data=CategoryCallbackFactory(name="Все вместе")
    )
    builder.button(
        text="Отмена", callback_data=CategoryCallbackFactory(name="Отмена", action="stop")
    )
    builder.adjust(3)
    return builder.as_markup()


def confirm_category_kb():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Подтвердить", callback_data=CategoryCallbackFactory(name="confirm")
    )
    builder.button(
        text="Отмена", callback_data=CategoryCallbackFactory(name="Отмена", action="stop")
    )
    return builder.as_markup()


