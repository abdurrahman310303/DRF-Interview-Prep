from rest_framework import viewsets, status, filters, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Post, Comment
from .serializers import (
    PostListSerializer, 
    PostDetailSerializer, 
    PostCreateUpdateSerializer,
    CommentSerializer,
    CommentCreateSerializer
)
from .permissions import IsAuthorOrReadOnly, IsCommentAuthorOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for Post model"""
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'author', 'categories']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'updated_at', 'title', 'views_count']
    lookup_field = 'slug'
    
    def get_queryset(self):
        """Return published posts for public, all posts for authenticated users"""
        if self.request.user.is_authenticated:
            return Post.objects.all()
        return Post.objects.filter(status='published')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, slug=None):
        """Publish a draft post"""
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {'error': 'Only the author can publish this post'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        post.status = 'published'
        post.save()
        return Response({'message': 'Post published successfully'})
    
    @action(detail=True, methods=['post'])
    def like(self, request, slug=None):
        """Like a post (simple implementation)"""
        post = self.get_object()
        # You could implement a Like model here
        return Response({'message': 'Post liked successfully'})

class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for Comment model"""
    queryset = Comment.objects.filter(is_approved=True)
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentAuthorOrReadOnly]
    
    def get_queryset(self):
        """Return comments for a specific post if post_id is provided"""
        post_id = self.request.query_params.get('post_id', None)
        if post_id:
            return Comment.objects.filter(post_id=post_id, is_approved=True)
        return Comment.objects.filter(is_approved=True)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostSearchView(generics.ListAPIView):
    """Advanced search view for posts"""
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Post.objects.filter(status='published')
        query = self.request.query_params.get('q', None)
        category = self.request.query_params.get('category', None)
        author = self.request.query_params.get('author', None)
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(excerpt__icontains=query)
            )
        
        if category:
            queryset = queryset.filter(categories__slug=category)
        
        if author:
            queryset = queryset.filter(author__username=author)
        
        return queryset.distinct()
