# import datetime
# import telebot
# from django.utils import timezone
#
# from TaroBot.models import TgUser, UserRequest, UserLimitModel, UnlimitedRequestsModel
#
#
# class LimitFilter(telebot.custom_filters.SimpleCustomFilter):
#     key = 'user_limit'
#
#     @staticmethod
#     def check(message, **kwargs):
#         try:
#             user = TgUser.objects.get(tg_id=message.from_user.id)
#         except TgUser.DoesNotExist:
#             TgUser.objects.create(
#                 tg_id=message.from_user.id,
#                 nickname=message.from_user.username,
#                 first_name=message.from_user.first_name,
#                 last_name=message.from_user.last_name
#             )
#             return True
#
#         if UnlimitedRequestsModel.objects.filter(user=user, end_datetime__gte=datetime.datetime.now()).exists():
#             return True
#         payment, created = UserLimitModel.objects.get_or_create(user=user)
#         return payment.request_limit >= 1
