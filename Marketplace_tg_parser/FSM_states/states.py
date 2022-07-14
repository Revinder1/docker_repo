from aiogram.dispatcher.fsm.state import StatesGroup, State


class CategoryForm(StatesGroup):
    # пока только сарафаны/платья, потом додумать
    category = State()
    size = State()
    discount = State()
    confirmed = State()



class AdminForm(StatesGroup):
    choosing = State()
    add = State()
    delete = State()
    confirmed_add = State()
    confirmed_delete = State()



