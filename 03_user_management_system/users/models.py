from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Custom User model with extended profile fields"""
    
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        MODERATOR = 'moderator', _('Moderator')
        USER = 'user', _('User')
    
    # Basic fields
    email = models.EmailField(unique=True, verbose_name=_('Email Address'))
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
        verbose_name=_('Role')
    )
    
    # Profile fields
    bio = models.TextField(blank=True, max_length=500, verbose_name=_('Bio'))
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        verbose_name=_('Profile Picture')
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Date of Birth')
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        verbose_name=_('Phone Number')
    )
    
    # Status fields
    is_verified = models.BooleanField(default=False, verbose_name=_('Email Verified'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    last_login_ip = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name=_('Last Login IP')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    
    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.username
    
    @property
    def is_admin(self):
        """Check if user is admin"""
        return self.role == self.Role.ADMIN
    
    @property
    def is_moderator(self):
        """Check if user is moderator"""
        return self.role == self.Role.MODERATOR or self.role == self.Role.ADMIN
    
    @property
    def full_name(self):
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def get_role_display_name(self):
        """Get human-readable role name"""
        return dict(self.Role.choices)[self.role]
