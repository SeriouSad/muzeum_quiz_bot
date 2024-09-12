import time

from django.db.models import Sum
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from museum_bot.bot.config import bot
from museum_bot.models import *
from museum_bot.bot.keyboards import *
from museum_bot.bot.states import *


def process_finish(user):
    return UserMuseumProgression.objects.filter(user=user, finished=True).count() >= 5

def process_progress(user):
    test_progression = UserMuseumProgression.objects.get(user=user, finished=False)
    if test_progression.questions_count == 15:
        test_progression.finished = True
        test_progression.save()
        return True
    return False

def send_answer(question, message, correct):
    if question.order == 15:
        kb = res_kb
    else:
        kb = next_kb
    if question.answer_description.photo:
        if correct:
            bot.send_photo(message.chat.id, question.answer_description.photo, caption=question.answer_description.text_correct, reply_markup=kb)
        else:
            bot.send_photo(message.chat.id, question.answer_description.photo,
                           caption=question.answer_description.text, reply_markup=kb)
    else:
        if correct:
            bot.send_message(message.chat.id, question.answer_description.text_correct, reply_markup=kb)
        else:
            bot.send_message(message.chat.id, question.answer_description.text, reply_markup=kb)


def send_question(user, message):
    if process_progress(user):
        if process_finish(user):
            bot.send_message(message.chat.id, "Поздравляем, ты прошел квест,  и справился со всеми заданиями. Чтобы узнать сколько у тебя звёзд, вызови команду /stars")
            bot.delete_state(user.tg_id, message.chat.id)
            return
        bot.send_message(message.chat.id, f"Вы успешно завершили этот тест, у вас сейчас {user.points}⭐️\n\nВыберите новый музей", reply_markup=museum_choice)
        bot.set_state(user.tg_id, AnswerStates.waiting_museum, message.chat.id)
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
    text = "Привет! Это проект *«Город Героев Москва»*. ⭐\n\nПри поддержке *Комитета общественных связей и молодежной политики города Москвы и Департамента культуры города Москвы*.\n\nМы подготовили для тебя серию квестов по историческим музеям столицы. Чтобы принять участие нажми на кнопку «Начать». 👇"
    bot.send_message(message.chat.id, text, reply_markup=reg_kb, parse_mode="Markdown")
    bot.set_state(message.from_user.id, RegistrationStates.start, message.chat.id)


@bot.callback_query_handler(func=lambda call: True, state=RegistrationStates.start)
def func(call: types.CallbackQuery):
    # bot.send_message(call.message.chat.id, bot.get_state(call.from_user.id, call.message.chat.id))
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Отлично! Всего пара действий и ты в игре. Для начала тебе *нужно зарегистрироваться*❗️\nНапиши в чате ФИО👇", parse_mode="Markdown")
    bot.set_state(call.from_user.id, RegistrationStates.fio, call.message.chat.id)


@bot.message_handler(state=RegistrationStates.fio)
def func(message: types.Message):
    user = TgUser.objects.get(tg_id=message.from_user.id)
    user.fio = message.text[:254]
    user.save()
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reg_button = types.KeyboardButton(text="Поделиться контактом", request_contact=True)
    keyboard.add(reg_button)
    bot.send_message(message.chat.id, "Отправьте свой *номер телефона*", reply_markup=keyboard, parse_mode="Markdown")
    bot.set_state(message.from_user.id, RegistrationStates.phone, message.chat.id)


@bot.message_handler(state=RegistrationStates.phone, content_types=['contact'])
def func(message: types.Message):
    user = TgUser.objects.get(tg_id=message.from_user.id)
    user.phone_number = message.contact.phone_number
    user.save()
    bot.send_message(message.chat.id, "Введите свой *email*", parse_mode="Markdown")
    bot.set_state(message.from_user.id, RegistrationStates.email, message.chat.id)


@bot.message_handler(state=RegistrationStates.phone)
def func(message: types.Message):
    user = TgUser.objects.get(tg_id=message.from_user.id)
    user.phone_number = message.text[:254]
    user.save()
    bot.send_message(message.chat.id, "Введите свой *email*", parse_mode="Markdown")
    bot.set_state(message.from_user.id, RegistrationStates.email, message.chat.id)


@bot.message_handler(state=RegistrationStates.email)
def func(message: types.Message):
    user = TgUser.objects.get(tg_id=message.from_user.id)
    user.email = message.text[:254]
    user.save()
    bot.send_message(message.chat.id,
                     "Необходимо принять *согласие об обработке персональных данных*", reply_markup=conf_kb, parse_mode="Markdown")
    bot.set_state(message.from_user.id, RegistrationStates.confirm, message.chat.id)


@bot.callback_query_handler(func=lambda call: True, state=RegistrationStates.confirm)
def func(call: types.CallbackQuery):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id,
                     "*Поздравляем!* 🎉 Теперь ты можешь следить за своими успехами в личном кабинете.\n\nА прямо сейчас ты можешь *ознакомиться с нашими правилами*.", reply_markup=rule_kb, parse_mode="Markdown")
    bot.set_state(call.from_user.id, RegistrationStates.rules, call.message.chat.id)


@bot.callback_query_handler(func=lambda call: True, state=RegistrationStates.rules)
def func(call: types.CallbackQuery):
    rules = Rules.objects.all().first()
    bot.send_message(call.message.chat.id, rules.text, parse_mode='HTML')
    bot.delete_state(call.from_user.id, call.message.chat.id)


@bot.message_handler(commands=['start_quiz'])
def func(message: types.Message):
    text = "Ну все, *мы начинаем*!\n\n➡️ *Выбери из списка музей*, в котором ты сейчас находишься или в который собираешься  отправиться в первую очередь!"
    bot.send_message(message.chat.id, text, reply_markup=museum_choice, parse_mode="Markdown")
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
        bot.send_message(call.message.chat.id, f"К сожалению, ответ неверный, но у меня есть подсказка\n\n{question.hint}")
        # TODO time.sleep(1)
        progress.hint_used = True
        progress.save()
        send_question(user, call.message)
        return
    else:
        bot.send_message(call.message.chat.id, "К сожалению, ответ неверный, ниже ты можешь увидеть правильный ответ.\n⬇️⬇️⬇️")
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



@bot.message_handler(commands=['prize'])
def func(message: types.Message):
    a = """
    🎁 <b>Результаты розыгрыша главного приза</b> ты можешь узнать <a href="https://t.me/gorodgeroevmsk">здесь</a> <b>13 октября 2024 года</b>.
    
<b>Весь мерч</b> будет доступен здесь: https://t.me/gorodgeroevmsk с 13 октября

Чтобы обменять свои звезды на призы, тебе <b>необходимо написать нашему администратору</b>. Для этого нажми на кнопку «Написать администратору»
При выборе призов, <b>учитывай свое количество баллов</b>. 

Для того <b>чтобы получить приз</b> тебе необходимо написать а чат следующее:
 1️⃣ Свой номер телефона
 2️⃣ Номера выбранных призов 
 3️⃣ Сумму звезд, которую ты на них тратишь. 

‼️После того, как администратор подтвердил наличие мерча, забрать призы можно будет по адресу: <b>Холодильный переулок 3к1с8</b>
    """
    bot.send_message(message.chat.id, a, parse_mode='HTML', reply_markup=mes_kb)


@bot.message_handler(commands=['account'])
def func(message: types.Message):
    user = TgUser.objects.get(tg_id=message.from_user.id)
    text = f"ФИО: {user.fio}\nНомер телефона: {user.phone_number}\nПочта: {user.email}\nКоличество звезд: {user.points}⭐️"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['stars'])
def func(message: types.Message):
    user = TgUser.objects.get(tg_id=message.from_user.id)
    text = f"Всего звезд: {user.points}⭐️"
    bot.send_message(message.chat.id, text)
    if user.points < 300:
        bot.send_message(message.chat.id, "Ты только посмотри сколько у тебя звёзд, все их можно обменять на стильный мерч вот здесь: ссылка")
    else:
        bot.send_message(message.chat.id, "Ура! У тебя рекордный результат! Так что предлагаем тебе принять участие в супер-игре, состоящей всего из трех вопросов. \n\nПобедители супер-игры будут участвовать в розыгрыше главного приза, который состоится ….. сентября. Обладатель приза будет определен с помощью генератора случайных чисел среди тех, кто правильно ответил на вопросы супер-игры.\n\nЕсли ты в игре, нажми на кнопку «В игре»", reply_markup=sp_game_kb)
        bot.set_state(message.chat.id, SPstates.start, message.from_user.id)


@bot.callback_query_handler(func=lambda call: True, state=SPstates.start)
def func(call: types.CallbackQuery):
    bot.answer_callback_query(call.id)
    text = """А теперь, чтобы получить к ней доступ, тебе ниже надо *написать цифровой шифр*.\n👉🏻 В каждом музее, ответом на супер-вопрос была цифра.\n*Подставь свои цифры в верной последовательности*, чтобы они соответствовали музеям:\n\nГБУК г. Москвы «Музей-панорама "Бородинская битва"»\nГБУК г. Москвы «Мемориальный музей космонавтики»\nГБУК r. Москвы «Музей истории ГУЛАГа»\nГБУК г. Москвы «Музей археологии Москвы»\nГБУК г. Москвы «Государственный музей обороны Москвы»"""
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    bot.set_state(call.from_user.id, SPstates.code, call.message.chat.id)


@bot.message_handler(state=SPstates.code)
def func(message: types.Message):
    if message.text == "15122117":
        bot.send_message(message.chat.id, "Что ж,  код подошел. Добро пожаловать в супер-игру!", reply_markup=sp_kb)
        bot.set_state(message.from_user.id, SPstates.start2, message.chat.id)
    else:
        bot.send_message(message.chat.id, "Нам жаль, но код не подходит! Попробуй еще раз расположить цифры в верной последовательности без пробелов.")


@bot.callback_query_handler(func=lambda call: True, state=SPstates.start2)
def func(call: types.CallbackQuery):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "1️⃣ В каком из этих музеев больше всего экспонатов?", reply_markup=question_kb1)
    bot.set_state(call.from_user.id, SPstates.question1, call.message.chat.id)


@bot.callback_query_handler(func=lambda call: True, state=SPstates.question1)
def func(call: types.CallbackQuery):
    bot.answer_callback_query(call.id)
    user = TgUser.objects.get(tg_id=call.from_user.id)
    result, created = SuperGameUser.objects.get_or_create(user=user)
    q_res = bool(int(call.data))
    if q_res:
        result.question1 = True
        result.save()
        bot.send_message(call.message.chat.id, "Верно!\n\nВ музее космонавтики в Москве представлено более 96 000 экспонатов.")
    else:
        bot.send_message(call.message.chat.id,
                         "Нам жаль, этот ответ неверный.\n\nВ музее космонавтики в Москве представлено более 96 000 экспонатов.")
    bot.send_message(call.message.chat.id, "2️⃣ Какой из музеев является самым молодым?", reply_markup=question_kb2)
    bot.set_state(call.from_user.id, SPstates.question2, call.message.chat.id)


@bot.callback_query_handler(func=lambda call: True, state=SPstates.question2)
def func(call: types.CallbackQuery):
    bot.answer_callback_query(call.id)
    user = TgUser.objects.get(tg_id=call.from_user.id)
    result = SuperGameUser.objects.get(user=user)
    q_res = bool(int(call.data))
    if q_res:
        result.question2 = True
        result.save()
        bot.send_message(call.message.chat.id, "Вы правы!\n\nМузей истории ГУЛАГа был открыт в июле 2001 года.")
    else:
        bot.send_message(call.message.chat.id,
                         "Нам жаль, этот ответ неверный.\n\nСамый молодой — Музей истории ГУЛАГа. Он был открыт в июле 2001 года.")
    bot.send_message(call.message.chat.id, "3️⃣ Какой музей выстроен вокруг одного из своих экспонатов?", reply_markup=question_kb3)
    bot.set_state(call.from_user.id, SPstates.question3, call.message.chat.id)


@bot.callback_query_handler(func=lambda call: True, state=SPstates.question3)
def func(call: types.CallbackQuery):
    bot.answer_callback_query(call.id)
    user = TgUser.objects.get(tg_id=call.from_user.id)
    result, created = SuperGameUser.objects.get_or_create(user=user)
    q_res = bool(int(call.data))
    if q_res:
        result.question3 = True
        result.save()
        bot.send_message(call.message.chat.id, "Да!\n\nМузей археологии Москвы — уникальный музей, построенный вокруг устоев древнего Воскресенского моста на месте реальных археологических раскопок.")
    else:
        bot.send_message(call.message.chat.id,
                         "Нам жаль, этот ответ неверный.\n\nМузей археологии Москвы — уникальный музей, построенный вокруг устоев древнего Воскресенского моста на месте реальных археологических раскопок.")

    if result.question3 and result.question1 and result.question2:
        bot.send_message(call.message.chat.id, "Поздравляем! Вы участвуете в розыгрыше призов на сайте: https://t.me/gorodgeroevmsk\n\nСовсем скоро мы объявим победителей.")
    else:
        bot.send_message(call.message.chat.id,
                         "Благодарим за участие в нашем квесте!")
    bot.delete_state(call.from_user.id, call.message.chat.id)
