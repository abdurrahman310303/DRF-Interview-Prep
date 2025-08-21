from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    """User registration view"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for the new user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            },
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        }, status=status.HTTP_201_CREATED)

class UserLoginView(TokenObtainPairView):
    """User login view with JWT tokens"""
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        # Update last login IP if available
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            user.last_login_ip = request.META['HTTP_X_FORWARDED_FOR']
        elif 'REMOTE_ADDR' in request.META:
            user.last_login_ip = request.META['REMOTE_ADDR']
        user.save()
        
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role
            },
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        })

class UserLogoutView(generics.GenericAPIView):
    """User logout view - blacklist refresh token"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({'message': 'Logout successful'})
        except Exception as e:
            return Response(
                {'error': 'Invalid token'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class ChangePasswordView(generics.UpdateAPIView):
    """Change password view"""
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({'message': 'Password changed successfully'})

class PasswordResetRequestView(generics.GenericAPIView):
    """Request password reset view"""
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        
        # Generate password reset token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # In production, send email here
        # For development, just return the token
        reset_url = f"http://localhost:3000/reset-password/{uid}/{token}/"
        
        return Response({
            'message': 'Password reset email sent',
            'reset_url': reset_url,  # Remove this in production
            'uid': uid,
            'token': token
        })

class PasswordResetConfirmView(generics.GenericAPIView):
    """Confirm password reset view"""
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer
    
    def post(self, request, uid, token):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Decode user ID
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
            
            # Check token validity
            if default_token_generator.check_token(user, token):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({'message': 'Password reset successful'})
            else:
                return Response(
                    {'error': 'Invalid token'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {'error': 'Invalid reset link'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class TokenRefreshView(TokenRefreshView):
    """Refresh JWT token view"""
    permission_classes = [AllowAny]
