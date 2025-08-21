from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Profile
from .serializers import (
    ProfileSerializer,
    ProfileUpdateSerializer,
    ProfilePrivacySerializer,
    ProfilePreferencesSerializer,
    PublicProfileSerializer
)
from users.permissions import IsOwnerOrReadOnly, IsOwnerOrAdmin

class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for Profile model"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ProfileUpdateSerializer
        elif self.action == 'update_privacy':
            return ProfilePrivacySerializer
        elif self.action == 'update_preferences':
            return ProfilePreferencesSerializer
        elif self.action == 'public':
            return PublicProfileSerializer
        return ProfileSerializer
    
    def get_queryset(self):
        """Return profiles based on user's role and privacy settings"""
        user = self.request.user
        
        if user.is_admin:
            return Profile.objects.all()
        elif user.is_moderator:
            # Moderators can see all profiles but not sensitive info
            return Profile.objects.all()
        else:
            # Regular users can only see public profiles
            return Profile.objects.filter(profile_public=True)
    
    @action(detail=True, methods=['patch'])
    def update_privacy(self, request, pk=None):
        """Update profile privacy settings"""
        profile = self.get_object()
        serializer = ProfilePrivacySerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'Privacy settings updated successfully',
            'profile': ProfileSerializer(profile).data
        })
    
    @action(detail=True, methods=['patch'])
    def update_preferences(self, request, pk=None):
        """Update profile preferences"""
        profile = self.get_object()
        serializer = ProfilePreferencesSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'Preferences updated successfully',
            'profile': ProfileSerializer(profile).data
        })
    
    @action(detail=True, methods=['get'])
    def public(self, request, pk=None):
        """Get public profile information"""
        profile = self.get_object()
        serializer = PublicProfileSerializer(profile)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        try:
            profile = request.user.profile
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """Profile detail view and update"""
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_object(self):
        return self.request.user.profile

class PublicProfileListView(generics.ListAPIView):
    """List all public profiles"""
    queryset = Profile.objects.filter(profile_public=True)
    serializer_class = PublicProfileSerializer
    permission_classes = [IsAuthenticated]

class ProfilePrivacyView(generics.UpdateAPIView):
    """Update profile privacy settings"""
    serializer_class = ProfilePrivacySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_object(self):
        return self.request.user.profile

class ProfilePreferencesView(generics.UpdateAPIView):
    """Update profile preferences"""
    serializer_class = ProfilePreferencesSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_object(self):
        return self.request.user.profile
