from rest_framework import serializers
from rest_framework.response import Response

from django.contrib.auth import authenticate


from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'id')  # noqa


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('staff_id', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return Response(user, status=200)
        raise serializers.ValidationError("Incorrect Credentials")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('fullname', 'staff_id', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            staff_id=validated_data['staff_id'],
            password=validated_data['password'],
            fullname=validated_data['fullname'],
        )
        return user


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class CodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniqueCode
        fields = '__all__'
