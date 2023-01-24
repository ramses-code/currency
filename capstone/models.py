from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_transactions')
    amount = models.FloatField()
    currancy_from = models.CharField(max_length=64)
    currancy_to = models.CharField(max_length=64)
    total = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s transaction"