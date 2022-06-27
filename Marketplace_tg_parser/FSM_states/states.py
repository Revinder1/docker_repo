from aiogram.dispatcher.fsm.state import StatesGroup, State


class CategoryForm(StatesGroup):
    # пока только сарафаны/платья, потом додумать
    category = State()
    size = State()
    discount = State()



