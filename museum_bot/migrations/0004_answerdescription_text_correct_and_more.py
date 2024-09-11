# Generated by Django 4.1.7 on 2024-09-11 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_bot', '0003_usermuseumprogression_hint_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='answerdescription',
            name='text_correct',
            field=models.TextField(blank=True, verbose_name='Текст правильного ответа, если ответ верный'),
        ),
        migrations.AlterField(
            model_name='answerdescription',
            name='text',
            field=models.TextField(blank=True, verbose_name='Текст правильного ответа'),
        ),
    ]