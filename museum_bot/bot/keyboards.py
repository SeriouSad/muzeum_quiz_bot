from django.db.utils import ProgrammingError
from telebot.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup

from museum_bot.models import Museum

start_kb = InlineKeyboardMarkup()
start_kb.add(InlineKeyboardButton("Начать", callback_data="start"))

next_kb = InlineKeyboardMarkup()
next_kb.add(InlineKeyboardButton("Следующий вопрос", callback_data="next"))

reg_kb = InlineKeyboardMarkup()
reg_kb.add(InlineKeyboardButton("Начать регистрацию", callback_data="reg"))

conf_kb = InlineKeyboardMarkup()
conf_kb.add(InlineKeyboardButton("Дать согласие", callback_data="conf"))

museum_choice = InlineKeyboardMarkup()
museums = Museum.objects.all()
for i in museums:
    museum_choice.add(InlineKeyboardButton(str(i.name), callback_data=str(i.id)))


sp_game_kb = InlineKeyboardMarkup()
sp_game_kb.add(InlineKeyboardButton("В игре", callback_data="sp"))