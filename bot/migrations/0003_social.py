# Generated by Django 5.0.7 on 2024-08-01 23:15

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_about_certificate_rule_photo_about_photo_certificate_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Social',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', ckeditor.fields.RichTextField(verbose_name='Post matni')),
            ],
            options={
                'verbose_name': 'Ijtimoiy tarmoqlar',
                'verbose_name_plural': 'Ijtimoiy tarmoqlar',
            },
        ),
    ]
