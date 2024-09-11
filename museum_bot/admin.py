from django.contrib import admin
from museum_bot.models import *

@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    pass

@admin.register(Museum)
class CategoryAdmin(admin.ModelAdmin):
    pass

class AnswerAdminInline(admin.TabularInline):
    model = Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (AnswerAdminInline,)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(UserMuseumProgression)
class UserCategoryProgressionAdmin(admin.ModelAdmin):
    pass

@admin.register(AnswerDescription)
class UserCategoryProgressionAdmin(admin.ModelAdmin):
    pass
