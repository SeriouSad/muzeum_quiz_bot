# Generated by Django 4.1.7 on 2024-09-13 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_bot', '0007_alter_tguser_tg_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tguser',
            name='username',
            field=models.CharField(default=None, max_length=255, null=True, verbose_name='Никнейм'),
        ),
    ]
