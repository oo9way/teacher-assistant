# Generated by Django 4.2.14 on 2024-08-11 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_telegramuser_is_teacher'),
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='groups', to='bot.telegramuser'),
        ),
        migrations.DeleteModel(
            name='GroupMember',
        ),
    ]
