# Generated by Django 4.1.7 on 2024-09-13 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_bot', '0006_supergameuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tguser',
            name='tg_id',
            field=models.CharField(max_length=255, verbose_name='Id пользователя в telegram'),
        ),
    ]
