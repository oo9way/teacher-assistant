# Generated by Django 4.2.14 on 2024-08-15 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_studenttask_is_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentanswer',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
    ]
