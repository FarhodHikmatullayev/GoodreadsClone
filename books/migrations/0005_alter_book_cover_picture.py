# Generated by Django 4.2.4 on 2023-08-28 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_book_cover_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_picture',
            field=models.ImageField(default='default_cower_picture.jpg', upload_to='books/image'),
        ),
    ]
