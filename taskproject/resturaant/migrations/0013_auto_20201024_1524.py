# Generated by Django 2.2 on 2020-10-24 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resturaant', '0012_auto_20201024_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_address', to='resturaant.Address'),
        ),
    ]
