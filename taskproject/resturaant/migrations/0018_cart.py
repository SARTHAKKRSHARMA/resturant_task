# Generated by Django 2.2 on 2020-10-24 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resturaant', '0017_auto_20201024_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('in_cart', 'In Cart'), ('done', 'Done')], max_length=25)),
                ('food_item', models.ManyToManyField(related_name='cart_items', to='resturaant.Food_Items')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='resturaant.Customer')),
            ],
        ),
    ]
