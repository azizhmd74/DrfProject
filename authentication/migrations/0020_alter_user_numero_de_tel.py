# Generated by Django 4.2.2 on 2023-06-26 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0019_alter_user_numero_de_tel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='numero_de_tel',
            field=models.IntegerField(null=True),
        ),
    ]
