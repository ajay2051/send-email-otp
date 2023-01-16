from django.db import models
from django.contrib.auth.models import AbstractUser
import time
# Create your models here.


class Users(AbstractUser):
    email = models.EmailField(unique=True)
    otp = models.IntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    time = models.FloatField(default=time.time())

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['']
