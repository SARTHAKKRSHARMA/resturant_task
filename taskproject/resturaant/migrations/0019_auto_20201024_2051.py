# Generated by Django 2.2 on 2020-10-24 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resturaant', '0018_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='food_item',
        ),
        migrations.AddField(
            model_name='cart',
            name='food_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='resturaant.Food_Items'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.CharField(choices=[('in_cart', 'In Cart'), ('done', 'Done')], default='in_cart', max_length=25),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_cart', to='resturaant.Customer'),
        ),
    ]
