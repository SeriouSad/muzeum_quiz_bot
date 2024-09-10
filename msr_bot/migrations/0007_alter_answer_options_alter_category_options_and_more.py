# Generated by Django 4.1.7 on 2024-09-06 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('msr_bot', '0006_tguser_is_superuser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'verbose_name': 'Ответ на вопрос', 'verbose_name_plural': 'Ответы на вопросы'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория вопроса', 'verbose_name_plural': 'Категории вопроса'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'Вопрос', 'verbose_name_plural': 'Вопросы'},
        ),
        migrations.AlterModelOptions(
            name='tguser',
            options={'verbose_name': 'Пользователь телеграм', 'verbose_name_plural': 'Пользователи телеграм'},
        ),
        migrations.AlterModelOptions(
            name='useranswer',
            options={'verbose_name': 'Ответ пользователя', 'verbose_name_plural': 'Ответы пользователей'},
        ),
        migrations.AlterModelOptions(
            name='usercategoryprogression',
            options={'verbose_name': 'Прогресс пользователя ', 'verbose_name_plural': 'Прогресс пользователей по категориям'},
        ),
    ]
