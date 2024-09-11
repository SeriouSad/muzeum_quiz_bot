import time

from django.db.models import Sum
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from museum_bot.bot.config import bot
from museum_bot.models import *
from museum_bot.bot.keyboards import *
from museum_bot.bot.states import *


def process_progress(user):
    test_progression = UserMuseumProgression.objects.get(user=user, finished=False)
    if test_progression.questions_count == 2:
        test_progression.finished = True
        test_progression.save()
        return True
    return False

def send_answer(question, message, correct):
    if question.answer_description.photo:
        bot.send_photo(message.chat.id, question.answer_description.photo, caption=question.answer_description.text, reply_markup=next_kb)
    else:
        bot.send_message(message.chat.id, question.answer_description.text, reply_markup=next_kb)


def send_question(user, message):
    if process_progress(user):
        bot.send_message(message.chat.id, f"Вы успешно завершили этот тест, у вас сейчас {user.points}⭐️")
        bot.delete_state(user.tg_id, message.chat.id)
        return
    test_progression = UserMuseumProgression.objects.get(user=user, finished=False)
    question = Question.objects.filter(museum=test_progression.museum).order_by("order")[test_progression.questions_count]
    answers = Answer.objects.filter(question=question)
    kb = InlineKeyboardMarkup()
    for i in answers:
        kb.add(InlineKeyboardButton(str(i.text), callback_data=i.id))
    if question.photo:
        bot.send_photo(message.chat.id, question.photo, caption=question.text, reply_markup=kb)
    else:
        bot.send_message(message.chat.id, question.text, reply_markup=kb)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    try:
        TgUser.objects.get(tg_id=message.from_user.id)
        # bot.send_message(message.chat.id, "Вы уже зарегистрировались, вы можете приступить к квизу")
    except TgUser.DoesNotExist:
        TgUser.objects.create(
            tg_id=message.from_user.id,
            username=message.from_user.username,
        )
    text = "Привет! Это проект «Город Героев Москва».\n\nПри поддержке Комитета общественных связей и молодежной политики города Москвы и Департамента культуры города Москвы.\n\nМы подготовили для тебя серию квестов по историческим музеям столицы. Чтобы принять участие нажми на кнопку «Начать»."
    bot.send_message(message.chat.id, text, reply_markup=reg_kb)
    bot.set_state(message.from_user.id, RegistrationStates.start, message.chat.id)


@bot.callback_query_handler(func=lambda call: True, state=RegistrationStates.start)
def func(call: types.CallbackQuery):
    # bot.send_message(call.message.chat.id, bot.get_state(call.from_user.id, call.message.chat.id))
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Отлично! Всего пара действий и ты в игре. Для начала тебе нужно "
                                           "зарегистрироваться.\nНапиши в чате ФИО")
    bot.set_state(call.from_user.id, RegistrationStates.fio, call.message.chat.id)


@bot.message_handler(state=RegistrationStates.fio)
def func(message: types.Message):
    user = TgUser.objects.get(tg_id=message.from_user.id)
    user.fio = message.text[:254]
    user.save()
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reg_button = types.KeyboardButton(text="Поделиться контактом", request_contact=True)
    keyboard.add(reg_button)
    bot.send_message(message.chat.id, "Отправьте свой номер телефона", reply_markup=keyboard)
    bot.set_state(message.from_user.id, RegistrationStates.phone, message.chat.id)


@bot.message_handler(state=RegistrationStates.phone, content_types=['contact'])
def func(message: types.Message):
    user = TgUser.objects.get(tg_id=message.from_user.id)
    user.phone_number = message.contact.phone_number
    user.save()
    bot.send_message(message.chat.id, "Введите свой email")
    bot.set_state(message.from_user.id, RegistrationStates.email, message.chat.id)


@bot.message_handler(state=RegistrationStates.email)
def func(message: types.Message):
    user = TgUser.objects.get(tg_id=message.from_user.id)
    user.email = message.text[:254]
    user.save()
    bot.send_message(message.chat.id,
                     "Необходимо принять согласие об обработке персональных данных", reply_markup=conf_kb)
    bot.set_state(message.from_user.id, RegistrationStates.confirm, message.chat.id)


@bot.callback_query_handler(func=lambda call: True, state=RegistrationStates.confirm)
def func(call: types.CallbackQuery):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id,
                     "Поздравляем! Теперь ты можешь следить за своими успехами в личном кабинете.\n\nА прямо сейчас ты можешь ознакомиться с нашими правилами.")
    bot.delete_state(call.from_user.id, call.message.chat.id)


@bot.message_handler(commands=['start_quiz'])
def func(message: types.Message):
    text = "Ну все, мы начинаем!\n\nВыбери из списка музей, в котором ты сейчас находишься или в который собираешься  отправиться в первую очередь!"
    bot.send_message(message.chat.id, text, reply_markup=museum_choice)
    bot.set_state(message.from_user.id, AnswerStates.waiting_museum, message.chat.id)


@bot.callback_query_handler(func=lambda call: True, state=AnswerStates.waiting_museum)
def func(call: types.CallbackQuery):
    bot.answer_callback_query(call.id)
    user = TgUser.objects.get(tg_id=call.from_user.id)
    try:
        progress = UserMuseumProgression.objects.get(user=user, museum_id=int(call.data))
        if progress.finished:
            bot.send_message(call.message.chat.id, "Вы уже прошли квиз этого музея\n\nВыберите другой", reply_markup=museum_choice)
            return
    except UserMuseumProgression.DoesNotExist:
        UserMuseumProgression.objects.create(user=user, museum_id=int(call.data))
    except UserMuseumProgression.MultipleObjectsReturned:
        bot.send_message(call.message.chat.id, "Вы уже проходите квиз другого музея. Выбрать новый не получится")
        send_question(user, call.message)
        return
    bot.set_state(call.from_user.id, AnswerStates.waiting_for_answer, call.message.chat.id)
    send_question(user, call.message)


@bot.callback_query_handler(func=lambda call: True, state=AnswerStates.waiting_for_answer)
def func(call: types.CallbackQuery):
    bot.answer_callback_query(call.id)
    user = TgUser.objects.get(tg_id=call.from_user.id)
    progress = UserMuseumProgression.objects.get(user=user, finished=False)
    question = Question.objects.filter(museum=progress.museum).order_by("order")[
        progress.questions_count]
    answer = Answer.objects.get(id=int(call.data))
    user_answer = UserAnswer.objects.create(user=user, question=question)
    if answer.correct:
        user.points += 5
        user_answer.correct = True
        user_answer.save()
        send_answer(question, call.message, True)
        progress.questions_count += 1
        progress.hint_used = False
        progress.save()
    elif answer.correct and progress.hint_used:
        user.points += 2
        user_answer.correct = True
        user_answer.save()
        send_answer(question, call.message, True)
        progress.questions_count += 1
        progress.hint_used = False
        progress.save()
    elif question.hint and not progress.hint_used:
        bot.send_message(call.message.chat.id, f"К сожалению ответ неверный, но у меня есть подсказка\n\n{question.hint}")
        # TODO time.sleep(1)
        progress.hint_used = True
        progress.save()
        send_question(user, call.message)
        return
    else:
        bot.send_message(call.message.chat.id, "К сожалению ответ неверный")
        send_answer(question, call.message, False)
        progress.questions_count += 1
        progress.hint_used = False
        progress.save()
    user.save()
    bot.set_state(call.from_user.id, AnswerStates.waiting_for_next_question, call.message.chat.id)



@bot.callback_query_handler(func=lambda call: True, state=AnswerStates.waiting_for_next_question)
def func(call: types.CallbackQuery):
    bot.answer_callback_query(call.id)
    user = TgUser.objects.get(tg_id=call.from_user.id)
    bot.set_state(call.from_user.id, AnswerStates.waiting_for_answer, call.message.chat.id)
    send_question(user, call.message)


@bot.message_handler(commands=['rules'])
def func(message: types.Message):
    rules = Rules.objects.all().first()
    bot.send_message(message.chat.id, rules.text, parse_mode='HTML')


@bot.message_handler(commands=['account'])
def func(message: types.Message):
    user = TgUser.objects.get(tg_id=message.from_user.id)
    text = f"ФИО: {user.fio}\nНомер телефона: {user.phone_number}\nПочта: {user.email}\nКоличество звезд: {user.points}⭐️"
    bot.send_message(message.chat.id, text)