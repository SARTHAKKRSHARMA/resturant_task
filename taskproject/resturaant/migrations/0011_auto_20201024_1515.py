# Generated by Django 2.2 on 2020-10-24 09:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('resturaant', '0010_auto_20201024_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food_items',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=15)),
                ('time_of_order', models.DateTimeField(default=django.utils.timezone.now)),
                ('order_status', models.CharField(choices=[('del', 'Delivered'), ('ndel', 'Not Delivered')], max_length=50)),
                ('item_ordered', models.ManyToManyField(to='resturaant.Food_Items')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_order', to='resturaant.Customer')),
            ],
        ),
    ]