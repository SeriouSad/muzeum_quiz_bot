from django.db.models import Sum
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from museum_bot.bot.config import bot
from museum_bot.models import *
from museum_bot.bot.keyboards import *
from museum_bot.bot.states import *


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    try:
        TgUser.objects.get(tg_id=message.from_user.id)
    except TgUser.DoesNotExist:
        TgUser.objects.create(
            tg_id=message.from_user.id,
            username=message.from_user.username,
        )
    text = "Тут будет главный текст"
    bot.send_message(message.chat.id, text, reply_markup=reg_kb)
    bot.set_state(message.from_user.id, RegistrationStates.start, message.chat.id)


@bot.callback_query_handler(func=lambda call: True, state=RegistrationStates.start)
def func(call: types.CallbackQuery):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Отлично! Всего пара действий и ты в игре. Для начала тебе нужно "
                                           "зарегистрироваться.\nНапиши в чате ФИО")
    bot.set_state(call.message.from_user.id, RegistrationStates.fio, call.message.chat.id)


@bot.message_handler(state=RegistrationStates.fio)
def func(message: types.Message):
    user = TgUser.objects.get(tg_id=message.from_user.id)
    user.fio = message.text[:255]
    user.save()
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    reg_button = types.KeyboardButton(text="Поделиться контактом", request_contact=True)
    keyboard.add(reg_button)
    bot.send_message(message.chat.id, "Отправьте свой номер телефона", reply_markup=keyboard)
    bot.set_state(message.from_user.id, RegistrationStates.phone, message.chat.id)
    