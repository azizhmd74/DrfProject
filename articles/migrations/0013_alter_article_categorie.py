# Generated by Django 4.2.2 on 2023-06-18 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_like_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='categorie',
            field=models.CharField(choices=[('Hommes', 'Hommes'), ('Femmes', 'Femmes'), ('Enfants', 'Enfants'), ('Sports', 'Sports')], max_length=20),
        ),
    ]