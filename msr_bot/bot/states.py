from telebot.handler_backends import State, StatesGroup


class StartStates(StatesGroup):
    start = State()

class AnswerStates(StatesGroup):
    waiting_for_answer = State()