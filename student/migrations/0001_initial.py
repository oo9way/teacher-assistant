# Generated by Django 4.2.14 on 2024-08-11 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bot', '0003_remove_notification_media_media_notification'),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('completed_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.telegramuser')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.task')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.telegramuser')),
            ],
        ),
    ]
