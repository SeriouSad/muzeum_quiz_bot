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
        bot.send_message(message.chat.id, "Вы уже зарегистрировались, вы можете приступить к квизу")
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
    user.fio = message.text[:254]
    user.save()
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    reg_button = types.KeyboardButton(text="Поделиться контактом", request_contact=True)
    keyboard.add(reg_button)
    bot.send_message(message.chat.id, "Отправьте свой номер телефона", reply_markup=keyboard)
    bot.set_state(message.from_user.id, RegistrationStates.phone, message.chat.id)


@bot.message_handler(state=RegistrationStates.phone, content_types=['contact'])
def func(message: types.Message):
    user = TgUser.objects.get(tg_id=message.from_user.id)
    user.phone = message.contact.phone_number
    user.save()
    bot.send_message(message.chat.id, "Введите свой email")
    bot.set_state(message.from_user.id, RegistrationStates.email, message.chat.id)


@bot.message_handler(state=RegistrationStates.email, content_types=['contact'])
def func(message: types.Message):
    user = TgUser.objects.get(tg_id=message.from_user.id)
    user.email = message.text[:254]
    user.save()
    bot.send_message(message.chat.id,
                     "Необходимо принять согласие об обработке персональных данных", reply_markup=conf_kb)
    bot.set_state(message.from_user.id, RegistrationStates.confirm, message.chat.id)


@bot.callback_query_handler(state=RegistrationStates.confirm)
def func(call: types.CallbackQuery):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Поздравляем! Теперь ты можешь следить за своими успехами в личном кабинете.\n\nА прямо сейчас ты можешь ознакомиться с нашими правилами.")
    bot.delete_state(call.message.from_user.id, call.message.chat.id)




    