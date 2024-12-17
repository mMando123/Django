from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    USER_ROLE_CHOICES = (
        ('regular_user', 'Regular User'),
        ('expert_user', 'Expert User'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)  # In years
    company = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username
