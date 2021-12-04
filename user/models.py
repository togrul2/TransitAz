from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_verified = models.BooleanField(default=False, help_text='Designates whether user verified his account through the link he received in email that backend sends after sign up')
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.username
