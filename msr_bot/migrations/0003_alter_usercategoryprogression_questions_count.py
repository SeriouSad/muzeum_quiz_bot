# Generated by Django 4.1.7 on 2024-09-05 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msr_bot', '0002_usercategoryprogression_finished_alter_question_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercategoryprogression',
            name='questions_count',
            field=models.IntegerField(default=0),
        ),
    ]
