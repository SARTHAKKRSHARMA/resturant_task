# Generated by Django 2.2 on 2020-10-27 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resturaant', '0039_auto_20201027_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food_items',
            name='end_time',
            field=models.TimeField(default='22:00:00'),
        ),
        migrations.AlterField(
            model_name='food_items',
            name='start_time',
            field=models.TimeField(default='08:00:00'),
        ),
    ]