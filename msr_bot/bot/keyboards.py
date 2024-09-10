from django.db.utils import ProgrammingError
from telebot.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup

start_kb = InlineKeyboardMarkup()
start_kb.add(InlineKeyboardButton("Начать", callback_data="start"))