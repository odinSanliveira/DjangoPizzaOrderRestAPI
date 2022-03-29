from asyncio.windows_events import NULL
from email.policy import default
from multiprocessing import AuthenticationError
from .models import User
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.db import models

from django.contrib import auth

class UserCreationSerializer(serializers.ModelSerializer):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=80, unique=True)
    password = serializers.CharField(min_length=8,write_only=True)
    image = models.ImageField(upload_to='static/media/profiles/', blank=True, null=True)
    class Meta:
        model = User
        fields=['username', 'email', 'image', 'password']
    
    def validate(self, attrs):
        username_exists = User.objects.filter(username=attrs['username']).exists()

        if username_exists:
            raise serializers.ValidationError(detail="Username already exists")
       
        email_exists = User.objects.filter(email=attrs['email']).exists()

        if email_exists:
            raise serializers.ValidationError(detail="Email already exists")

       
        return super().validate(attrs)
        

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            image = validated_data['image']
        )
        user.set_password(validated_data['password'])

        user.save()
        return user

class UsernameUpdateSerializer(serializers.ModelSerializer):
    username = models.CharField(max_length=25, unique=True)

    class Meta:
        model = User 
        fields = ['username']



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=80, min_length=3)
    password = serializers.CharField(max_length=68, min_length=8,write_only=True)
    username = serializers.CharField(max_length=25, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only = True)
    

    class Meta:
        model = User
        fields=['email', 'password','tokens','username']        

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_verified:
            raise AuthenticationFailed('Email not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }