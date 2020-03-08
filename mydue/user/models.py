from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField
import uuid
import os


def get_file_path(instance, filename,):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('pro_pics/', filename)    

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False,error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    is_verified = models.BooleanField(default=False)
    phone = PhoneField(blank=True, help_text='Contact phone number')



