# Generated by Django 3.2 on 2022-05-11 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prof', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='username',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='username'),
        ),
    ]
