from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.conf import settings
import telebot
from msr_bot.bot.handlers import bot


def index(request):
    if request.method == "POST":
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])
    return HttpResponse(status=200)


