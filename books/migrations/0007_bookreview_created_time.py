# Generated by Django 4.2.4 on 2023-08-29 10:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_alter_book_cover_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookreview',
            name='created_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]