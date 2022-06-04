# Generated by Django 3.2 on 2022-05-02 00:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('followship', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followrequests',
            name='from_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='following_req', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='followrequests',
            name='to_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='follow_req', to=settings.AUTH_USER_MODEL),
        ),
    ]
