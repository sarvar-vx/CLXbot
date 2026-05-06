from aiogram.fsm.state import State, StatesGroup


class AddProduct(StatesGroup):
    type = State()
    name = State()
    message_ids = State()


class EditProduct(StatesGroup):
    search = State()
    field = State()
    value = State()


class DeleteProduct(StatesGroup):
    search = State()
    confirm = State()


class AddChannel(StatesGroup):
    name = State()
    username = State()


class DeleteChannel(StatesGroup):
    search = State()
    confirm = State()

class Login(StatesGroup):
    password = State()

class Broadcast(StatesGroup):
    message = State()