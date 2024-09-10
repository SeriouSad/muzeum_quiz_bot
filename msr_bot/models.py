from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)  # Название категории
    question_count = models.IntegerField()   # Количество вопросов в категории
    score = models.IntegerField()        # Максимальное количество баллов за категорию
    time_limit = models.IntegerField()       # Время на категорию в секундах
    order = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории вопроса'
        verbose_name = "Категория вопроса"


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    photo = models.ImageField(upload_to='staticfiles/questions/photo/', blank=True)
    file = models.FileField(upload_to='staticfiles/questions/file/', blank=True)
    correct_answer = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.correct_answer = self.correct_answer.lower()
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.text[:50]} - {self.category.name}"

    class Meta:
        verbose_name_plural = 'Вопросы'
        verbose_name = "Вопрос"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Ответы на вопросы'
        verbose_name = "Ответ на вопрос"


class TgUser(models.Model):
    tg_id = models.IntegerField()
    username = models.CharField(max_length=255)
    is_superuser = models.BooleanField(default=False)

    objects = models.Manager()
    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = 'Пользователи телеграм'
        verbose_name = "Пользователь телеграм"


class UserAnswer(models.Model):
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    text_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.question}"

    class Meta:
        verbose_name_plural = 'Ответы пользователей'
        verbose_name = "Ответ пользователя"


class UserCategoryProgression(models.Model):
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    questions_count = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.name}"

    class Meta:
        verbose_name_plural = 'Прогресс пользователей по категориям'
        verbose_name = "Прогресс пользователя "

