# Generated by Django 3.2.5 on 2021-07-19 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_usermodel_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='user_type',
            field=models.CharField(max_length=15, verbose_name='User type'),
        ),
    ]
