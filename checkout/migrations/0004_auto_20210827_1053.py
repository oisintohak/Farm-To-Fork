# Generated by Django 3.2.6 on 2021-08-27 05:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('checkout', '0003_order_product_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='FarmerOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('farmer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='farmer_orders', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='farmer_orders', to='checkout.order', unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='orderlineitem',
            name='farmer_order',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='lineitems', to='checkout.farmerorder'),
        ),
    ]
