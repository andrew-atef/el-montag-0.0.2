from django.db import models
from django.contrib.auth.models import User
import uuid 

# Create your models here.
class Verification_code(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=10, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.code = uuid.uuid4().hex[:6].upper()
        super().save(*args, **kwargs)