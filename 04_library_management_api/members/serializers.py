from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Member


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id', 'username']


class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()
    borrowing_limit = serializers.ReadOnlyField()
    
    class Meta:
        model = Member
        fields = [
            'id', 'user', 'membership_id', 'membership_level', 'membership_date',
            'expiry_date', 'phone', 'address', 'date_of_birth', 'is_active',
            'full_name', 'borrowing_limit', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'membership_id', 'membership_date', 'created_at', 'updated_at']


class MemberRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    
    class Meta:
        model = Member
        fields = [
            'username', 'password', 'first_name', 'last_name', 'email',
            'membership_level', 'expiry_date', 'phone', 'address', 'date_of_birth'
        ]
    
    def create(self, validated_data):
        # Extract user data
        user_data = {
            'username': validated_data.pop('username'),
            'password': validated_data.pop('password'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'email': validated_data.pop('email'),
        }
        
        # Create user
        user = User.objects.create_user(**user_data)
        
        # Create member
        member = Member.objects.create(user=user, **validated_data)
        return member
