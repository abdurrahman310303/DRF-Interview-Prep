from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    """Extended user profile with additional information"""
    
    class Gender(models.TextChoices):
        MALE = 'male', _('Male')
        FEMALE = 'female', _('Female')
        OTHER = 'other', _('Other')
        PREFER_NOT_TO_SAY = 'prefer_not_to_say', _('Prefer not to say')
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('User')
    )
    
    # Personal Information
    gender = models.CharField(
        max_length=20,
        choices=Gender.choices,
        blank=True,
        verbose_name=_('Gender')
    )
    address = models.TextField(blank=True, verbose_name=_('Address'))
    city = models.CharField(max_length=100, blank=True, verbose_name=_('City'))
    state = models.CharField(max_length=100, blank=True, verbose_name=_('State'))
    country = models.CharField(max_length=100, blank=True, verbose_name=_('Country'))
    postal_code = models.CharField(max_length=20, blank=True, verbose_name=_('Postal Code'))
    
    # Professional Information
    company = models.CharField(max_length=200, blank=True, verbose_name=_('Company'))
    job_title = models.CharField(max_length=200, blank=True, verbose_name=_('Job Title'))
    website = models.URLField(blank=True, verbose_name=_('Website'))
    linkedin = models.URLField(blank=True, verbose_name=_('LinkedIn'))
    twitter = models.URLField(blank=True, verbose_name=_('Twitter'))
    
    # Preferences
    timezone = models.CharField(max_length=50, default='UTC', verbose_name=_('Timezone'))
    language = models.CharField(max_length=10, default='en', verbose_name=_('Language'))
    notification_email = models.BooleanField(default=True, verbose_name=_('Email Notifications'))
    notification_sms = models.BooleanField(default=False, verbose_name=_('SMS Notifications'))
    
    # Privacy Settings
    profile_public = models.BooleanField(default=True, verbose_name=_('Public Profile'))
    show_email = models.BooleanField(default=False, verbose_name=_('Show Email'))
    show_phone = models.BooleanField(default=False, verbose_name=_('Show Phone'))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    
    class Meta:
        db_table = 'profiles'
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
    
    def __str__(self):
        return f"Profile of {self.user.username}"
    
    def get_full_address(self):
        """Get formatted full address"""
        address_parts = []
        if self.address:
            address_parts.append(self.address)
        if self.city:
            address_parts.append(self.city)
        if self.state:
            address_parts.append(self.state)
        if self.postal_code:
            address_parts.append(self.postal_code)
        if self.country:
            address_parts.append(self.country)
        
        return ', '.join(address_parts) if address_parts else 'No address provided'
    
    def get_social_links(self):
        """Get available social media links"""
        links = {}
        if self.website:
            links['website'] = self.website
        if self.linkedin:
            links['linkedin'] = self.linkedin
        if self.twitter:
            links['twitter'] = self.twitter
        return links
