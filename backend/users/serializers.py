from rest_framework import serializers
from .models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'profile_picture', 'bio', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'is_donor', 'is_recruiter',
            'is_investigator', 'is_coordinator', 'is_sponsor', 'is_researcher',
            'phone_number', 'date_of_birth', 'address', 'organization', 'profile',
            'is_active', 'date_joined'
        ]
        read_only_fields = ['is_active', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data.pop('password', None),
            **validated_data
        )
        UserProfile.objects.create(user=user)
        return user


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'password', 'first_name', 'last_name', 'is_donor', 'is_recruiter',
            'is_investigator', 'is_coordinator', 'is_sponsor', 'is_researcher',
            'phone_number', 'date_of_birth', 'address', 'organization'
        ]
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data.pop('password'),
            **validated_data
        )
        UserProfile.objects.create(user=user)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number', 'date_of_birth', 
            'address', 'organization', 'is_donor', 'is_recruiter',
            'is_investigator', 'is_coordinator', 'is_sponsor', 'is_researcher'
        ]


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']
