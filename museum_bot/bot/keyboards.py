from django.db.utils import ProgrammingError
from telebot.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup

start_kb = InlineKeyboardMarkup()
start_kb.add(InlineKeyboardButton("Начать", callback_data="start"))

next_kb = InlineKeyboardMarkup()
next_kb.add(InlineKeyboardButton("Следующий вопрос", callback_data="next"))

reg_kb = InlineKeyboardMarkup()
reg_kb.add(InlineKeyboardButton("Начать регистрацию", callback_data="reg"))