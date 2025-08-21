from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model"""
    user_username = serializers.ReadOnlyField(source='user.username')
    user_email = serializers.ReadOnlyField(source='user.email')
    full_address = serializers.ReadOnlyField()
    social_links = serializers.ReadOnlyField()
    
    class Meta:
        model = Profile
        fields = [
            'id', 'user_username', 'user_email', 'gender', 'address',
            'city', 'state', 'country', 'postal_code', 'company',
            'job_title', 'website', 'linkedin', 'twitter', 'timezone',
            'language', 'notification_email', 'notification_sms',
            'profile_public', 'show_email', 'show_phone', 'full_address',
            'social_links', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating profile information"""
    class Meta:
        model = Profile
        fields = [
            'gender', 'address', 'city', 'state', 'country', 'postal_code',
            'company', 'job_title', 'website', 'linkedin', 'twitter',
            'timezone', 'language', 'notification_email', 'notification_sms',
            'profile_public', 'show_email', 'show_phone'
        ]

class ProfilePrivacySerializer(serializers.ModelSerializer):
    """Serializer for updating privacy settings"""
    class Meta:
        model = Profile
        fields = [
            'profile_public', 'show_email', 'show_phone'
        ]

class ProfilePreferencesSerializer(serializers.ModelSerializer):
    """Serializer for updating user preferences"""
    class Meta:
        model = Profile
        fields = [
            'timezone', 'language', 'notification_email', 'notification_sms'
        ]

class PublicProfileSerializer(serializers.ModelSerializer):
    """Serializer for public profile view (respects privacy settings)"""
    user_username = serializers.ReadOnlyField(source='user.username')
    user_email = serializers.SerializerMethodField()
    user_phone = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = [
            'id', 'user_username', 'user_email', 'user_phone',
            'gender', 'city', 'state', 'country', 'company',
            'job_title', 'website', 'linkedin', 'twitter',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_user_email(self, obj):
        """Only show email if user allows it"""
        if obj.show_email:
            return obj.user.email
        return None
    
    def get_user_phone(self, obj):
        """Only show phone if user allows it"""
        if obj.show_phone:
            return obj.user.phone_number
        return None
    
    def to_representation(self, instance):
        """Filter out private information"""
        data = super().to_representation(instance)
        
        # Remove fields that are not public
        if not instance.profile_public:
            return {'id': data['id'], 'user_username': data['user_username']}
        
        # Remove None values
        return {k: v for k, v in data.items() if v is not None}
