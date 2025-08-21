from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'created_at', 'posts_count']
    
    def get_posts_count(self, obj):
        return obj.posts.count()

class CategoryCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating categories"""
    class Meta:
        model = Category
        fields = ['name', 'description']
