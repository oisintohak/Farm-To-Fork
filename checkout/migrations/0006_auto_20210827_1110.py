# Generated by Django 3.2.6 on 2021-08-27 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0005_alter_farmerorder_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmerorder',
            name='farmer_order_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='farmerorder',
            name='product_count',
            field=models.IntegerField(default=0),
        ),
    ]
