# Generated by Django 2.2 on 2020-10-27 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resturaant', '0041_auto_20201027_1518'),
    ]

    operations = [
        migrations.CreateModel(
            name='DaysOfTheWeek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_the_week', models.CharField(choices=[('Monday', '0'), ('Tuesday', '1'), ('Wednesday', '2'), ('Thursday', '3'), ('Friday', '4'), ('Saturday', '5'), ('Friday', '6')], max_length=15)),
            ],
        ),
    ]