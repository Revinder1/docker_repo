from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder



def get_admin_kb_reply():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Добавить в БД"))
    builder.add(types.KeyboardButton(text="Удалить из БД"))
    builder.add(types.KeyboardButton(text="Отмена"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def admin_confirm_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Подтвердить"))
    builder.add(types.KeyboardButton(text="Отменить"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
