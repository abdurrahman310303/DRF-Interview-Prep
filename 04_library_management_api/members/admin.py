from django.contrib import admin
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['membership_id', 'get_full_name', 'membership_level', 'membership_date', 'expiry_date', 'is_active']
    list_filter = ['membership_level', 'is_active', 'membership_date', 'expiry_date']
    search_fields = ['membership_id', 'user__first_name', 'user__last_name', 'user__email', 'phone']
    readonly_fields = ['membership_id', 'membership_date', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.full_name
    get_full_name.short_description = 'Full Name'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Membership Details', {
            'fields': ('membership_id', 'membership_level', 'membership_date', 'expiry_date', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('phone', 'address', 'date_of_birth')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
