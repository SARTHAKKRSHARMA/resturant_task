# Generated by Django 2.2 on 2020-10-25 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resturaant', '0030_delete_coupons'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_user', models.CharField(choices=[('both', 'Both'), ('normal', 'Normal'), ('premium', 'Premium')], default='premium', max_length=15)),
                ('coupon_name', models.CharField(blank=True, max_length=20, null=True)),
                ('coupon_description', models.TextField(blank=True, null=True)),
                ('coupon_code', models.CharField(max_length=20)),
                ('percent_discount', models.DecimalField(decimal_places=2, max_digits=4)),
                ('expiry_date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
