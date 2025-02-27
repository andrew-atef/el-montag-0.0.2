# Generated by Django 4.0.2 on 2022-03-07 19:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('affiliate', '0002_alter_affiliate_profile_affiliate_code_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transfer_amount', models.CharField(max_length=10)),
                ('number1', models.CharField(max_length=11)),
                ('status', models.CharField(choices=[('قيد المراجعه', 'قيد المراجعه'), ('تم التحويل', 'تم التحويل'), ('خطا فى التحويل', 'خطا فى التحويل')], max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
