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
        text="Сарафаны", callback_data=CategoryCallbackFactory(name="Сарафаны1")
    )
    builder.button(
        text="Платья", callback_data=CategoryCallbackFactory(name="Платья1")
    )
    builder.button(
        text="Все категории", callback_data=CategoryCallbackFactory(name="Все категории1")
    )
    builder.button(
        text="Отмена", callback_data=CategoryCallbackFactory(name="Отмена1", action="stop")
    )
    builder.adjust(3)
    return builder.as_markup()


#
# def get_keyboard():
#     buttons = [
#         [
#             types.InlineKeyboardButton(text="Сарафаны", callback_data="sundresses"),
#             types.InlineKeyboardButton(text="Платья", callback_data="dresses"),
#             types.InlineKeyboardButton(text="Все категории", callback_data="all_cats")
#         ],
#         [types.InlineKeyboardButton(text="Отмена", callback_data="stop")]
#     ]
#     keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
#     return keyboard
