from django.contrib.auth.models import AbstractUser
from django.db import models

# extending the existing data model:
class CustomUser(AbstractUser):
    my_stocks = models.JSONField(default=list)  # Stores a list of stock symbols
