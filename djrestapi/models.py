
from django.db import models
from rest_framework.authtoken.models import Token 
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone

class UserAccessInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ipaddress = models.GenericIPAddressField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)


class Book(models.Model):
    book_name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
