from django.contrib import admin 
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'completed','due_date', 'created_at']
    list_filter = ['completed', 'due_date','created_at']
    search_fields = ['title', 'description','user__username']
    readonly_fields = ['created_at', 'updated_at']