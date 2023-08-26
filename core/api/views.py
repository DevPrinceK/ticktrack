# django
from django.shortcuts import render
from django.contrib.auth import login
from api.serializers import LoginSerializer, UserSerializer

# rest framework
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer

# knox
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView


class OverviewAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({
            "message": "The API for TickTrack is running successfully",
            "endpoints": [
                {"endpoint": "/", "description": "returns the overview of the entire api infrastructure"},
                {"endpoint": "/login", "description": "used to login the user"},
                {"endpoint": "/logout", "description": "used to logout the current user from the current device"},
                {"endpoint": "/logoutall", "description": "used to logout current user from all devices"},
            ]
        })


class LoginAPI(KnoxLoginView):
    '''For handling user logins'''
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        '''Uses the post method to login the user'''
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        # Delete token - this will logout any other users using this account
        AuthToken.objects.filter(user=user).delete()
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1],
        }, status=status.HTTP_200_OK)
