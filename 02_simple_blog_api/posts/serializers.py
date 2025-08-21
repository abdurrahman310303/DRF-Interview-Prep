from rest_framework import serializers
from .models import Post, Comment
from users.serializers import UserSerializer
from categories.serializers import CategorySerializer
from categories.models import Category

class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at', 'updated_at', 'is_approved']
        read_only_fields = ['created_at', 'updated_at', 'author', 'is_approved']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class PostListSerializer(serializers.ModelSerializer):
    """Serializer for listing posts (summary view)"""
    author = UserSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    excerpt = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'excerpt', 'author', 'categories', 'status', 'featured_image', 'created_at', 'views_count']
    
    def get_excerpt(self, obj):
        return obj.get_excerpt()

class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed post view"""
    author = UserSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    excerpt = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'excerpt', 'author', 'categories', 'status', 'featured_image', 'created_at', 'updated_at', 'published_at', 'views_count', 'comments']
    
    def get_excerpt(self, obj):
        return obj.get_excerpt()

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating posts"""
    categories = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Category.objects.all(),
        required=False
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'categories', 'status', 'featured_image']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class CommentCreateSerializer(serializers.Serializer):
    """Serializer for creating comments"""
    content = serializers.CharField()
