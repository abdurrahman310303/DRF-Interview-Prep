from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'bio', 'phone_number'
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        user = authenticate(
            username=attrs['username'],
            password=attrs['password']
        )
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')
        attrs['user'] = user
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile data"""
    full_name = serializers.ReadOnlyField()
    role_display = serializers.ReadOnlyField(source='get_role_display_name')
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'bio', 'profile_picture', 'date_of_birth',
            'phone_number', 'role', 'role_display', 'is_verified',
            'is_active', 'last_login', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'username', 'email', 'role', 'is_verified',
            'is_active', 'last_login', 'created_at', 'updated_at'
        ]

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'bio', 'profile_picture',
            'date_of_birth', 'phone_number'
        ]

class UserRoleUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user role (admin only)"""
    class Meta:
        model = User
        fields = ['role']
    
    def validate_role(self, value):
        user = self.context['request'].user
        if not user.is_admin:
            raise serializers.ValidationError("Only admins can change user roles")
        return value

class UserListSerializer(serializers.ModelSerializer):
    """Serializer for listing users (public information)"""
    full_name = serializers.ReadOnlyField()
    role_display = serializers.ReadOnlyField(source='get_role_display_name')
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'full_name', 'bio', 'profile_picture',
            'role_display', 'is_verified', 'is_active', 'created_at'
        ]

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for requesting password reset"""
    email = serializers.EmailField()
    
    def validate_email(self, value):
        if not User.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError("No active user found with this email address")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for confirming password reset"""
    token = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
