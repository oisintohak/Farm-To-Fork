# Generated by Django 3.2.5 on 2021-07-19 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=40, verbose_name='First name')),
                ('last_name', models.CharField(max_length=40, verbose_name='Last name')),
                ('user_type', models.CharField(choices=[('Customers', 'Customer'), ('Farmers', 'Farmer')], max_length=20, verbose_name='User type')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('street_address1', models.CharField(blank=True, max_length=80, null=True)),
                ('street_address2', models.CharField(blank=True, max_length=80, null=True)),
                ('town_or_city', models.CharField(blank=True, max_length=40, null=True)),
                ('county', models.CharField(blank=True, max_length=80, null=True)),
                ('postcode', models.CharField(blank=True, max_length=20, null=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
