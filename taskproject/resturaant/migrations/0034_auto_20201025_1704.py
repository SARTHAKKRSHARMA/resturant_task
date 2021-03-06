# Generated by Django 2.2 on 2020-10-25 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resturaant', '0033_mealitem_meals'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meals',
            name='food_item',
        ),
        migrations.RemoveField(
            model_name='meals',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='meals',
            name='user',
        ),
        migrations.AddField(
            model_name='meals',
            name='type_of_user',
            field=models.CharField(choices=[('both', 'Both'), ('normal', 'Normal'), ('premium', 'Premium')], default='premium', max_length=20),
        ),
    ]
