from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_verified = models.BooleanField(default=False, help_text='Designates whether user verified his account through the link he received in email that backend sends after sign up')

    def __str__(self):
        return self.username
