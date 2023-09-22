from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, validators=[MinLengthValidator(11)])
    national_id = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
