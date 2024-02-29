from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)



