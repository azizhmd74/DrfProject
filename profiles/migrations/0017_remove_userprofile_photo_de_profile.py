# Generated by Django 4.2.2 on 2023-06-18 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0016_rename_profile_picture_userprofile_photo_de_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='photo_de_profile',
        ),
    ]
