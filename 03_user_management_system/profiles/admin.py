from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'gender', 'city', 'country', 'company', 'job_title',
        'profile_public', 'created_at'
    ]
    list_filter = [
        'gender', 'profile_public', 'notification_email', 'notification_sms',
        'created_at', 'updated_at'
    ]
    search_fields = [
        'user__username', 'user__email', 'user__first_name', 'user__last_name',
        'company', 'job_title', 'city', 'country'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('gender', 'date_of_birth')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code')
        }),
        ('Professional Information', {
            'fields': ('company', 'job_title', 'website', 'linkedin', 'twitter')
        }),
        ('Preferences', {
            'fields': ('timezone', 'language', 'notification_email', 'notification_sms')
        }),
        ('Privacy Settings', {
            'fields': ('profile_public', 'show_email', 'show_phone')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['make_profiles_public', 'make_profiles_private', 'enable_email_notifications', 'disable_email_notifications']
    
    def make_profiles_public(self, request, queryset):
        """Make selected profiles public"""
        updated = queryset.update(profile_public=True)
        self.message_user(request, f'{updated} profiles were successfully made public.')
    make_profiles_public.short_description = "Make selected profiles public"
    
    def make_profiles_private(self, request, queryset):
        """Make selected profiles private"""
        updated = queryset.update(profile_public=False)
        self.message_user(request, f'{updated} profiles were successfully made private.')
    make_profiles_private.short_description = "Make selected profiles private"
    
    def enable_email_notifications(self, request, queryset):
        """Enable email notifications for selected profiles"""
        updated = queryset.update(notification_email=True)
        self.message_user(request, f'{updated} profiles had email notifications enabled.')
    enable_email_notifications.short_description = "Enable email notifications"
    
    def disable_email_notifications(self, request, queryset):
        """Disable email notifications for selected profiles"""
        updated = queryset.update(notification_email=False)
        self.message_user(request, f'{updated} profiles had email notifications disabled.')
    disable_email_notifications.short_description = "Disable email notifications"
