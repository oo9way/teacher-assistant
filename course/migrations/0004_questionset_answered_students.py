# Generated by Django 4.2.14 on 2024-08-15 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_telegramuser_is_teacher'),
        ('course', '0003_alter_questionset_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionset',
            name='answered_students',
            field=models.ManyToManyField(related_name='answered_question_sets', to='bot.telegramuser'),
        ),
    ]
