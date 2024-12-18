from django.contrib.auth.models import AbstractUser
from django.db import models

# extending the existing data model:
class CustomUser(AbstractUser):
    my_stocks = models.JSONField(default=list)
    my_coins = models.JSONField(default=list)
    user_updates = models.JSONField(default=dict)
    user_notifications = models.JSONField(default=list)
    last_action_datetime_utc = models.JSONField(default=str)
    
class CryptoCoinNames(models.Model):
    coin_name = models.CharField(max_length=255)