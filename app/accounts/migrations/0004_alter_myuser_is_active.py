# Generated by Django 3.2 on 2022-05-08 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20220502_0500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]