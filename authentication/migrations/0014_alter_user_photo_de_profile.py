# Generated by Django 4.2.2 on 2023-06-18 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0013_alter_user_photo_de_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo_de_profile',
            field=models.ImageField(default='img/default-thumbnail.jpg', upload_to='img/profile/'),
        ),
    ]