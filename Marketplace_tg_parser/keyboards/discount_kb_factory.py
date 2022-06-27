from aiogram import types
from typing import Optional
from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder



class DiscountCallbackFactory(CallbackData, prefix="disc"):
    discount: str
    action: Optional[str]


def get_discount_kb_fab():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="до 30%", callback_data=DiscountCallbackFactory(discount="до 30%")
    )
    builder.button(
        text="30-60%", callback_data=DiscountCallbackFactory(discount="30-60%")
    )
    builder.button(
        text="60% и больше", callback_data=DiscountCallbackFactory(discount="60% и больше")
    )
    builder.button(
        text="Отмена", callback_data=DiscountCallbackFactory(discount="Отмена", action="stop")
    )
    builder.adjust(3)
    return builder.as_markup()
