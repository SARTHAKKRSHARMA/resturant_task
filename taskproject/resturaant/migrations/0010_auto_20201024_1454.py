# Generated by Django 2.2 on 2020-10-24 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resturaant', '0009_auto_20201024_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food_items',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]