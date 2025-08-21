from rest_framework import viewsets, generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import User
from .serializers import (
    UserProfileSerializer,
    UserUpdateSerializer,
    UserRoleUpdateSerializer,
    UserListSerializer
)
from .permissions import (
    IsOwnerOrReadOnly,
    IsAdminUser,
    IsModeratorUser,
    IsOwnerOrAdmin
)

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model"""
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active', 'is_verified']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['username', 'first_name', 'last_name', 'created_at', 'last_login']
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action == 'update_role':
            return UserRoleUpdateSerializer
        elif self.action == 'list':
            return UserListSerializer
        return UserProfileSerializer
    
    def get_queryset(self):
        """Return users based on user's role"""
        user = self.request.user
        
        if user.is_admin:
            return User.objects.all()
        elif user.is_moderator:
            # Moderators can see all users but not sensitive info
            return User.objects.all()
        else:
            # Regular users can only see public information
            return User.objects.filter(is_active=True)
    
    @action(detail=True, methods=['patch'])
    def update_role(self, request, pk=None):
        """Update user role (admin only)"""
        user = self.get_object()
        serializer = UserRoleUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'User role updated successfully',
            'user': UserProfileSerializer(user).data
        })
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate/deactivate user (admin only)"""
        user = self.get_object()
        if not request.user.is_admin:
            return Response(
                {'error': 'Only admins can activate/deactivate users'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        user.is_active = not user.is_active
        user.save()
        
        action = 'activated' if user.is_active else 'deactivated'
        return Response({
            'message': f'User {action} successfully',
            'user': UserProfileSerializer(user).data
        })
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Verify user email (admin only)"""
        user = self.get_object()
        if not request.user.is_admin:
            return Response(
                {'error': 'Only admins can verify users'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        user.is_verified = True
        user.save()
        
        return Response({
            'message': 'User verified successfully',
            'user': UserProfileSerializer(user).data
        })
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get user statistics (admin only)"""
        if not request.user.is_admin:
            return Response(
                {'error': 'Only admins can view statistics'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        verified_users = User.objects.filter(is_verified=True).count()
        admin_users = User.objects.filter(role='admin').count()
        moderator_users = User.objects.filter(role='moderator').count()
        regular_users = User.objects.filter(role='user').count()
        
        return Response({
            'total_users': total_users,
            'active_users': active_users,
            'verified_users': verified_users,
            'admin_users': admin_users,
            'moderator_users': moderator_users,
            'regular_users': regular_users
        })

class UserProfileView(generics.RetrieveUpdateAPIView):
    """User profile view and update"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_object(self):
        return self.request.user

class UserListView(generics.ListAPIView):
    """List all users (public information only)"""
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role']
    search_fields = ['username', 'first_name', 'last_name']
    ordering_fields = ['username', 'created_at']

class AdminUserManagementView(generics.ListAPIView):
    """Admin view for managing all users"""
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active', 'is_verified']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['username', 'created_at', 'last_login']
