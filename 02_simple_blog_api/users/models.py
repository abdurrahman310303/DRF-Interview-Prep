from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom User model"""
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, max_length=500)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.username
