# Generated by Django 4.1.7 on 2024-09-05 15:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('msr_bot', '0004_question_correct_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='msr_bot.answer'),
        ),
        migrations.AddField(
            model_name='useranswer',
            name='text_answer',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usercategoryprogression',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]