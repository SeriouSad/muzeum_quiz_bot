# Generated by Django 4.1.7 on 2024-09-11 00:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Museum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Музей',
                'verbose_name_plural': 'Музеи',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, verbose_name='Текст вопроса')),
                ('photo', models.ImageField(blank=True, upload_to='staticfiles/questions/photo/', verbose_name='Фото')),
                ('hint', models.TextField(blank=True, verbose_name='Подсказка')),
                ('order', models.IntegerField(blank=True, default=None, null=True, verbose_name='Порядковый номер')),
                ('museum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='museum_bot.museum', verbose_name='Музей')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='TgUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_id', models.IntegerField(verbose_name='Id пользователя в telegram')),
                ('username', models.CharField(max_length=255, verbose_name='Никнейм')),
                ('fio', models.CharField(max_length=255, verbose_name='ФИО')),
                ('phone_number', models.CharField(max_length=255, verbose_name='Номер телефона')),
                ('email', models.CharField(max_length=255, verbose_name='email')),
                ('points', models.IntegerField(blank=True, default=0, verbose_name='Количество очков')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='UserMuseumProgression',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questions_count', models.IntegerField(default=0, verbose_name='Количество отвеченных вопросов')),
                ('finished', models.BooleanField(default=False, verbose_name='Закончен?')),
                ('museum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='museum_bot.museum', verbose_name='Музей')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='museum_bot.tguser', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Прогресс пользователя',
                'verbose_name_plural': 'Прогресс пользователей по музеям',
            },
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct', models.BooleanField(default=False, verbose_name='Верный?')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='museum_bot.question', verbose_name='Вопрос')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='museum_bot.tguser', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Ответ пользователя',
                'verbose_name_plural': 'Ответы пользователей',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Текст вопроса')),
                ('correct', models.BooleanField(default=False, verbose_name='Верный?')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='museum_bot.question', verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'Ответ на вопрос',
                'verbose_name_plural': 'Ответы на вопросы',
            },
        ),
    ]
