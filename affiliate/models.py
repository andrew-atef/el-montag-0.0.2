from django.db import models
from django.contrib.auth.models import User
import uuid 

# Create your models here.
class Affiliate_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notes = models.TextField(max_length=1000)
    affiliate_code = models.CharField(max_length=10, unique=True)
    affiliate_coupon = models.CharField(max_length=10, unique=True)
    withdrawn = models.CharField(max_length=10 )

    def save(self, *args, **kwargs):
        self.affiliate_code = uuid.uuid4().hex[:6].upper()
        self.affiliate_coupon = uuid.uuid4().hex[:6].upper()
        super().save(*args, **kwargs)

class Billing(models.Model):
    all_status = (
        ('قيد المراجعه','قيد المراجعه'),
        ('تم التحويل','تم التحويل'),
        ('خطا فى التحويل','خطا فى التحويل'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    transfer_amount = models.CharField(max_length=10)
    number1 = models.CharField(max_length=11)
    status = models.CharField(max_length=50, choices=all_status)

    created = models.DateTimeField(auto_now_add=True)