# Generated by Django 2.2 on 2020-10-27 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resturaant', '0037_food_items_max_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food_items',
            old_name='max_quantity',
            new_name='quantity_available',
        ),
    ]