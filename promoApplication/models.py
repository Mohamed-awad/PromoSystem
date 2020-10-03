from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class User(User):
    name = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    is_admin = models.BooleanField(default=False)


class Promo(models.Model):
    promo_type = models.CharField(max_length=20)
    promo_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    promo_amount = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)
    description = models.TextField()
    user = models.ForeignKey(User, null=True,  on_delete=models.CASCADE, limit_choices_to={'is_admin': False},)

    class Meta:
        ordering = ('-created_at',)

