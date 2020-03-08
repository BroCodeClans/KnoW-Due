from django.db import models
from user.models import User
import uuid
import os


def get_file_path(instance, filename,):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('provider_icons/', filename)

class Provider(models.Model):
    name = models.CharField(max_length=64)
    icon = models.ImageField(default='default.jpg',upload_to=get_file_path ,max_length=255, null=True, blank=True)

class Services(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=64,null=False, blank=False)
    message_id = models.CharField(max_length=64,null=False, blank=False, unique=True)
    bill_id = models.CharField(max_length=64)
    due_date = models.DateField(null=True,blank=True)
    amount = models.IntegerField(null=True,blank=True)
    # month = models.CharField(max_length=15)

class Voucher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    voucher_name = models.CharField(max_length=64)
    expiry_date = models.DateField()
    amount = models.IntegerField()

class Expenditure(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.IntegerField()
    month = models.DateField()
