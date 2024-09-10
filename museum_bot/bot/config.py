import logging
import telebot
from django.conf import settings
from telebot import custom_filters, StateMemoryStorage

state_storage = StateMemoryStorage()

bot = telebot.TeleBot(settings.BOT_TOKEN, state_storage=state_storage)
bot.set_webhook(settings.WEBHOOK_URL)
bot.add_custom_filter(custom_filters.StateFilter(bot))
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)