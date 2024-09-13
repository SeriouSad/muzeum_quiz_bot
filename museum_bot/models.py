from email.policy import default

from django.db import models


class TgUser(models.Model):
    tg_id = models.CharField(verbose_name="Id пользователя в telegram", max_length=255)
    username = models.CharField(max_length=255, verbose_name="Никнейм", null=True, default=None)
    fio = models.CharField(max_length=255, verbose_name="ФИО")
    phone_number = models.CharField(max_length=255, verbose_name="Номер телефона")
    email = models.CharField(max_length=255, verbose_name="email")
    points = models.IntegerField(verbose_name="Количество очков", blank=True, default=0)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.fio} - {self.username}"


class Museum(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Музеи'
        verbose_name = "Музей"


class AnswerDescription(models.Model):
    text = models.TextField(verbose_name="Текст правильного ответа", blank=True)
    photo = models.ImageField(upload_to='staticfiles/questions/photo/', blank=True, verbose_name="Фото")
    text_correct = models.TextField(verbose_name="Текст правильного ответа, если ответ верный", blank=True)

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name_plural = 'Комментарии к ответам'
        verbose_name = "Комментарий к ответам"

class Question(models.Model):
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE, verbose_name="Музей")
    text = models.TextField(blank=True, verbose_name="Текст вопроса")
    photo = models.ImageField(upload_to='staticfiles/questions/photo/', blank=True, verbose_name="Фото")
    hint = models.TextField(verbose_name="Подсказка", blank=True)
    order = models.IntegerField(verbose_name="Порядковый номер", blank=True, default=None, null=True)
    answer_description = models.ForeignKey(AnswerDescription, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Комментарий к ответам")


    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = Question.objects.filter(museum=self.museum).count() + 1
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.text[:50]} - {self.museum.name}"

    class Meta:
        verbose_name_plural = 'Вопросы'
        verbose_name = "Вопрос"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    text = models.CharField(max_length=255, verbose_name="Текст вопроса")
    correct = models.BooleanField(default=False, verbose_name="Верный?")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Ответы на вопросы'
        verbose_name = "Ответ на вопрос"


class UserAnswer(models.Model):
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    correct = models.BooleanField(default=False, verbose_name="Верный?")

    def __str__(self):
        return f"{self.user.username} - {self.question}"

    class Meta:
        verbose_name_plural = 'Ответы пользователей'
        verbose_name = "Ответ пользователя"


class UserMuseumProgression(models.Model):
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE, verbose_name="Музей")
    questions_count = models.IntegerField(default=0, verbose_name="Количество отвеченных вопросов")
    finished = models.BooleanField(default=False, verbose_name="Закончен?")
    hint_used = models.BooleanField(default=False, verbose_name="Использована подсказка?")

    def __str__(self):
        return f"{self.user.username} - {self.museum.name}"

    class Meta:
        verbose_name_plural = 'Прогресс пользователей по музеям'
        verbose_name = "Прогресс пользователя"


class Rules(models.Model):
    text = models.TextField(verbose_name="Текст правил")

    def __str__(self):
        return "Правила"

    class Meta:
        verbose_name_plural = 'Правила'
        verbose_name = "Правила"


class SuperGameUser(models.Model):
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    question1 = models.BooleanField(verbose_name="На вопрос 1 ответил корректно?", default=False)
    question2 = models.BooleanField(verbose_name="На вопрос 1 ответил корректно?", default=False)
    question3 = models.BooleanField(verbose_name="На вопрос 1 ответил корректно?", default=False)
    winner = models.BooleanField(verbose_name="Победил в супер-игре?", default=False)

    def __str__(self):
        return self.user.fio