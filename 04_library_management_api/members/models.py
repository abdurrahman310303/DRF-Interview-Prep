from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Member(models.Model):
    MEMBERSHIP_LEVELS = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
    ]
    
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message='Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.'
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_id = models.CharField(max_length=20, unique=True)
    membership_level = models.CharField(max_length=10, choices=MEMBERSHIP_LEVELS, default='basic')
    membership_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    phone = models.CharField(max_length=17, validators=[phone_validator])
    address = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['user__last_name', 'user__first_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.membership_id})"
    
    @property
    def borrowing_limit(self):
        limits = {
            'basic': 3,
            'premium': 5,
            'vip': 10
        }
        return limits.get(self.membership_level, 3)
    
    def save(self, *args, **kwargs):
        if not self.membership_id:
            # Generate membership ID
            last_member = Member.objects.order_by('id').last()
            if last_member:
                last_id = int(last_member.membership_id.split('LIB')[1])
                self.membership_id = f'LIB{last_id + 1:05d}'
            else:
                self.membership_id = 'LIB00001'
        super().save(*args, **kwargs)
