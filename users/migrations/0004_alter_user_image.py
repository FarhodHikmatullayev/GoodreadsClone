# Generated by Django 4.2.4 on 2023-08-28 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='default_profile_image.png', upload_to='users/images'),
        ),
    ]