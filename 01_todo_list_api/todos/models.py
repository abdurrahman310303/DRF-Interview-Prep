from django.db import models
from django.conf import settings  # NOT django.contrib.conf

class Todo(models.Model):
    """Todo item model"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'todos'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title