from telebot.handler_backends import State, StatesGroup


class RegistrationStates(StatesGroup):
    start = State()
    fio = State()
    phone = State()
    email = State()
    confirm = State()


class StartStates(StatesGroup):
    start = State()


class AnswerStates(StatesGroup):
    waiting_museum = State()
    waiting_for_answer = State()
    waiting_for_next_question = State()