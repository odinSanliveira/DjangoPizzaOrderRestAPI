from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from . import serializers

from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from . utils import Util
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
import jwt
from django.conf import settings
from rest_framework.permissions import IsAuthenticated


class HelloAuthView(generics.GenericAPIView):
    def get(self, request):
        return Response(data={"message":"Hello Auth"}, status=status.HTTP_200_OK)

class UserCreateView(generics.GenericAPIView):
    
    serializer_class = serializers.UserCreationSerializer
        
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)        

        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            user_signup = User.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user_signup).access_token

            current_site = str(get_current_site(request))
            relative_link = reverse('email_verification')
            absolute_url = "http://"+current_site+relative_link+"?token="+str(token)
            email_body= "Hi "+ user_signup.username + " use the link below to verify your email. \n" + 'validation link: '+ absolute_url
            message = {
                'domain': absolute_url, 
                'email_subject': 'verify your email address',
                'email_body': email_body,
                'to_email': user_signup.email}
            Util.send_email(message)
            return Response(data=user_data, status= status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

                return Response({'email': 'Successfully verified'}, status= status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status= status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid Token'}, status= status.HTTP_400_BAD_REQUEST)


class UpdateUsername(generics.GenericAPIView):
    serializer_class= serializers.UsernameUpdateSerializer
    permission_classes = [IsAuthenticated]
    def put(self, request, user_id):
        user = get_object_or_404(User, pk = user_id)

        data=request.data
        serializer = self.serializer_class(data=data, instance=user)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):

    serializer_class = serializers.LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
