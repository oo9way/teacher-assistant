# Generated by Django 4.2.14 on 2024-08-15 03:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_alter_question_question_set_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='course.lesson'),
        ),
    ]
