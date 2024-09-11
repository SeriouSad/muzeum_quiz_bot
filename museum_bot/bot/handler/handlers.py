# import json
# import time
# from datetime import datetime, timezone
# from django.conf import settings
# from django.db.models import Sum
# from telebot import types
# from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
#
# from msr_bot.bot.config import bot
# from msr_bot.models import *
# from msr_bot.bot.keyboards import start_kb
# from msr_bot.bot.states import AnswerStates, StartStates
#
#
# def calculate_time(user):
#     try:
#         test_progression = UserCategoryProgression.objects.get(user=user, finished=False)
#     except UserCategoryProgression.DoesNotExist:
#         return True
#     start_time_utc = test_progression.start_time.replace(tzinfo=timezone.utc)
#     current_time_utc = datetime.now(timezone.utc)
#
#     # Вычисляем разницу в секундах
#     seconds_passed = (current_time_utc - start_time_utc).total_seconds()
#     return seconds_passed < test_progression.category.time_limit
#
#
# def send_finish(user, message):
#     total_points = UserAnswer.objects.filter(user=user).aggregate(Sum('points'))
#     print(total_points)
#     bot.send_message(message.chat.id, f"Тест завершен. Вы набрали {total_points['points__sum']} баллов.")
#     bot.delete_state(message.from_user.id, message.chat.id)
#
#
# def process_progress(user):
#     try:
#         test_progression = UserCategoryProgression.objects.get(user=user, finished=False)
#     except UserCategoryProgression.DoesNotExist:
#         return True
#     if test_progression.questions_count == test_progression.category.question_count:
#         test_progression.finished = True
#         test_progression.save()
#         print(test_progression.category.order == 6)
#         if test_progression.category.order == 6:
#             return True
#         UserCategoryProgression.objects.create(user=user,
#                                                category=Category.objects.get(order=test_progression.category.order + 1))
#     return False
#
#
# def send_question(user, message):
#     process_progress(user)
#     try:
#         test_progression = UserCategoryProgression.objects.get(user=user, finished=False)
#     except UserCategoryProgression.DoesNotExist:
#         return True
#     question = Question.objects.filter(category=test_progression.category)[test_progression.questions_count]
#     answers = Answer.objects.filter(question=question)
#     kb = InlineKeyboardMarkup()
#     if answers.exists():
#         for i in answers:
#             kb.add(InlineKeyboardButton(str(i.text), callback_data=i.id))
#     if question.photo:
#         bot.send_photo(message.chat.id, question.photo, caption=question.text, reply_markup=kb)
#     elif question.file:
#         bot.send_document(message.chat.id, question.file, caption=question.text, reply_markup=kb)
#     else:
#         bot.send_message(message.chat.id, question.text, reply_markup=kb)
#
#     test_progression.start_time = datetime.now()
#     test_progression.save()
#
#
# @bot.message_handler(commands=['start'])
# def start(message: types.Message):
#     try:
#         user = TgUser.objects.get(tg_id=message.from_user.id)
#     except TgUser.DoesNotExist:
#         user = TgUser.objects.create(
#             tg_id=message.from_user.id,
#             username=message.from_user.username,
#         )
#     text = "Привет! Готов приступить к квизу?"
#     bot.send_message(message.chat.id, text, reply_markup=start_kb)
#     bot.set_state(message.from_user.id, StartStates.start, message.chat.id)
#
#
# @bot.message_handler(commands=['calculate_results'])
# def start(message: types.Message):
#     try:
#         user = TgUser.objects.get(tg_id=message.from_user.id)
#     except TgUser.DoesNotExist:
#         user = TgUser.objects.create(
#             tg_id=message.from_user.id,
#             username=message.from_user.username,
#         )
#     if not user.is_superuser:
#         return False
#     user_ranking = list(
#         UserAnswer.objects.values('user')
#         .annotate(total_points=Sum('points'))
#         .order_by('-total_points')
#     )[:10]
#
#     text = ""
#
#     for i in user_ranking:
#         user = TgUser.objects.get(id=i['user'])
#         text += f"{user_ranking.index(i) + 1}. @{user.username}. Итоговые баллы {i['total_points']}\n"
#     bot.send_message(message.chat.id, text)
#
#
# @bot.message_handler(state=AnswerStates.waiting_for_answer)
# def func(message: types.Message):
#     user = TgUser.objects.get(tg_id=message.from_user.id)
#     process_progress(user)
#     test_progression = UserCategoryProgression.objects.get(user=user, finished=False)
#     question = Question.objects.filter(category=test_progression.category)[test_progression.questions_count]
#     answer = message.text.lower()
#     user_answer = UserAnswer.objects.create(user=user, question=question)
#     if question.correct_answer == answer and calculate_time(user):
#         user_answer.points = question.category.score
#         user_answer.correct = True
#         user_answer.save()
#     elif question.correct_answer == answer and not calculate_time(user):
#         bot.send_message(message.chat.id, "К сожалению время этого запроса вышло. Баллы не будут засчитаны")
#     user_answer.text_answer = answer
#     user_answer.save()
#     test_progression.questions_count += 1
#     test_progression.save()
#     if process_progress(user):
#         send_finish(user, message)
#     send_question(user, message)
#
#
# @bot.callback_query_handler(func=lambda call: True, state=AnswerStates.waiting_for_answer)
# def func(call: types.CallbackQuery):
#     bot.answer_callback_query(call.id)
#     user = TgUser.objects.get(tg_id=call.from_user.id)
#     process_progress(user)
#     test_progression = UserCategoryProgression.objects.get(user=user, finished=False)
#     question = Question.objects.filter(category=test_progression.category)[test_progression.questions_count]
#     answer = Answer.objects.get(id=int(call.data))
#     user_answer = UserAnswer.objects.create(user=user, question=question)
#
#     if answer.correct and calculate_time(user):
#         user_answer.points = question.category.score
#         user_answer.correct = True
#         user_answer.save()
#     elif answer.correct and not calculate_time(user):
#         bot.send_message(call.message.chat.id, "К сожалению время этого запроса вышло. Баллы не будут засчитаны")
#     user_answer.answer = answer
#     user_answer.save()
#     test_progression.questions_count += 1
#     test_progression.save()
#     if process_progress(user):
#         send_finish(user, call.message)
#     send_question(user, call.message)
#
#
# @bot.callback_query_handler(func=lambda call: True, state=StartStates.start)
# def func(call: types.CallbackQuery):
#     user = TgUser.objects.get(tg_id=call.from_user.id)
#     try:
#         UserCategoryProgression.objects.get(user=user, finished=False)
#     except UserCategoryProgression.DoesNotExist:
#         UserCategoryProgression.objects.create(
#             user=user,
#             category=Category.objects.all().first()
#         )
#     bot.set_state(call.from_user.id, AnswerStates.waiting_for_answer, call.message.chat.id)
#     send_question(user, call.message)
#     bot.answer_callback_query(call.id)
