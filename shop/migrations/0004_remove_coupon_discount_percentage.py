# Generated by Django 4.0.2 on 2022-03-06 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_features_alter_product_desc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='discount_percentage',
        ),
    ]
