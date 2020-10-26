# Generated by Django 2.2 on 2020-10-24 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resturaant', '0008_food_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='food_category',
            name='type_of_category',
            field=models.CharField(choices=[('veg', 'Vegetarian'), ('non-veg', 'Non-Vegetarian')], default='veg', max_length=30),
        ),
        migrations.CreateModel(
            name='Food_Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(upload_to='')),
                ('price', models.FloatField()),
                ('item_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_item', to='resturaant.Food_Category')),
            ],
        ),
    ]