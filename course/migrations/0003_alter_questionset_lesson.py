# Generated by Django 4.2.14 on 2024-08-15 00:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_remove_question_lesson_questionset_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionset',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='course.lesson'),
        ),
    ]
