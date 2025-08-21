from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = [
        'username', 'email', 'first_name', 'last_name', 'role',
        'is_verified', 'is_active', 'is_staff', 'created_at'
    ]
    list_filter = [
        'role', 'is_verified', 'is_active', 'is_staff', 'is_superuser',
        'created_at', 'last_login'
    ]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'bio']
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('bio', 'profile_picture', 'date_of_birth', 'phone_number')
        }),
        ('Role & Status', {
            'fields': ('role', 'is_verified', 'last_login_ip')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login_ip']
    
    actions = ['verify_users', 'activate_users', 'deactivate_users', 'make_admin', 'make_moderator']
    
    def verify_users(self, request, queryset):
        """Mark selected users as verified"""
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} users were successfully verified.')
    verify_users.short_description = "Mark selected users as verified"
    
    def activate_users(self, request, queryset):
        """Activate selected users"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users were successfully activated.')
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        """Deactivate selected users"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users were successfully deactivated.')
    deactivate_users.short_description = "Deactivate selected users"
    
    def make_admin(self, request, queryset):
        """Make selected users admin"""
        updated = queryset.update(role='admin')
        self.message_user(request, f'{updated} users were successfully made admin.')
    make_admin.short_description = "Make selected users admin"
    
    def make_moderator(self, request, queryset):
        """Make selected users moderator"""
        updated = queryset.update(role='moderator')
        self.message_user(request, f'{updated} users were successfully made moderator.')
    make_moderator.short_description = "Make selected users moderator"
