from django.db.utils import ProgrammingError
from telebot.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup

from museum_bot.models import Museum

start_kb = InlineKeyboardMarkup()
start_kb.add(InlineKeyboardButton("Начать", callback_data="start"))

next_kb = InlineKeyboardMarkup()
next_kb.add(InlineKeyboardButton("Следующий вопрос", callback_data="next"))

reg_kb = InlineKeyboardMarkup()
reg_kb.add(InlineKeyboardButton("Начать", callback_data="reg"))

conf_kb = InlineKeyboardMarkup()
conf_kb.add(InlineKeyboardButton("Дать согласие", callback_data="conf"))

museum_choice = InlineKeyboardMarkup()
museums = Museum.objects.all()
for i in museums:
    museum_choice.add(InlineKeyboardButton(str(i.name), callback_data=str(i.id)))


sp_game_kb = InlineKeyboardMarkup()
sp_game_kb.add(InlineKeyboardButton("В игре", callback_data="sp"))

rule_kb = InlineKeyboardMarkup()
rule_kb.add(InlineKeyboardButton("Посмотреть правила", callback_data="rules"))


res_kb = InlineKeyboardMarkup()
res_kb.add(InlineKeyboardButton("Посмотреть результат", callback_data="rules"))

question_kb1 = InlineKeyboardMarkup()
question_kb1.add(InlineKeyboardButton("Музей-панорама «Бородинская битва»", callback_data="0"))
question_kb1.add(InlineKeyboardButton("Мемориальный музей космонавтики", callback_data="1"))
question_kb1.add(InlineKeyboardButton("Музей истории ГУЛАГа", callback_data="0"))
question_kb1.add(InlineKeyboardButton("Музей археологии Москвы", callback_data="0"))
question_kb1.add(InlineKeyboardButton("Государственный музей обороны Москвы", callback_data="0"))


question_kb2 = InlineKeyboardMarkup()
question_kb2.add(InlineKeyboardButton("Музей-панорама «Бородинская битва»", callback_data="0"))
question_kb2.add(InlineKeyboardButton("Мемориальный музей космонавтики", callback_data="0"))
question_kb2.add(InlineKeyboardButton("Музей истории ГУЛАГа", callback_data="1"))
question_kb2.add(InlineKeyboardButton("Музей археологии Москвы", callback_data="0"))
question_kb2.add(InlineKeyboardButton("Государственный музей обороны Москвы", callback_data="0"))

question_kb3 = InlineKeyboardMarkup()
question_kb3.add(InlineKeyboardButton("Музей-панорама «Бородинская битва»", callback_data="0"))
question_kb3.add(InlineKeyboardButton("Мемориальный музей космонавтики", callback_data="0"))
question_kb3.add(InlineKeyboardButton("Музей истории ГУЛАГа", callback_data="0"))
question_kb3.add(InlineKeyboardButton("Музей археологии Москвы", callback_data="1"))
question_kb3.add(InlineKeyboardButton("Государственный музей обороны Москвы", callback_data="0"))


mes_kb = InlineKeyboardMarkup()
mes_kb.add(InlineKeyboardButton("Написать администратору", callback_data="asd", url="https://vk.com/im?media=&sel=-222920535"))

sp_kb = InlineKeyboardMarkup()
sp_kb.add(InlineKeyboardButton("Начать супер-игру", callback_data='asd'))


