# Generated by Django 2.2 on 2020-10-24 12:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resturaant', '0015_auto_20201024_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_of_website',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_of_website', to=settings.AUTH_USER_MODEL),
        ),
    ]