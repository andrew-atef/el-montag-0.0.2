# Generated by Django 4.0.2 on 2022-03-06 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affiliate_profile',
            name='affiliate_code',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='affiliate_profile',
            name='affiliate_coupon',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
