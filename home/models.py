from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Interest(models.Model):
    category = models.TextField(default='business')
    sources = models.TextField(default='bbc-news')
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PaidUsers(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    valid_until = models.DateTimeField(null=True)


class Tokens(models.Model):
    token = models.TextField
    validity = models.IntegerField(default=1)




