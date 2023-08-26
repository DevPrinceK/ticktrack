# django
from django.shortcuts import render
from django.contrib.auth import login
from api.models import Course, Student
from api.serializers import CourseSerializer, StudentSerializer, UserSerializer

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
                {"endpoint": "/", "description": "returns the overview of the entire api infrastructure"}, #noqa
                {"endpoint": "/login", "description": "used to login the user"}, # noqa
                {"endpoint": "/logout","description": "used to logout the current user from the current device"}, # noqa
                {"endpoint": "/logoutall", "description": "used to logout current user from all devices"}, # noqa
                {"endpoint": "/courses", "description": "Used to get, create, update and delete courses"}, # noqa
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
            "message": "Login Successful",
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1],
        }, status=status.HTTP_200_OK)


class CRUDCourse(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''Used to get all courses created by user'''
        courses = Course.objects.filter(lecturer=request.user)
        return Response({
            "courses": CourseSerializer(courses, many=True).data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''Used to create a new course'''
        course_code = request.data.get("course_code")
        course_name = request.data.get("course_name")
        obj = Course.objects.create(
            course_code=course_code,
            course_name=course_name,
            lecturer=request.user
        )
        return Response({
            "message": "Course Created Successfully",
            "course": CourseSerializer(obj).data
        }, status=status.HTTP_201_CREATED)
        
        
    def put(self, request,*args, **kwargs):
        '''Used to update a course'''
        user = request.user
        course_id = request.data.get("course_id")
        course_code = request.data.get("course_code")
        course_name = request.data.get("course_name")
        obj = Course.objects.filter(id=course_id, lecturer=user).first()
        # check of course exists
        if obj is None:
            return Response({
                "message": "Course Fot Found"
            }, status=status.HTTP_404_NOT_FOUND)
        # check if course belongs to user
        obj.course_code = course_code
        obj.course_name = course_name
        obj.save()
        return Response({
            "message": "Course Updated Successfully",
            "course": CourseSerializer(obj).data
        }, status=status.HTTP_200_OK)
        
    def delete(self, request, *args, **kwargs):
        '''Used to delete a course'''
        user = request.user
        course_id = request.data.get("course_id")
        obj = Course.objects.filter(id=course_id, lecturer=user).first()
        # check of course exists
        if obj is None:
            return Response({
                "message": "Course Fot Found"
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            obj.delete()
            return Response({
                "message": "Course Deleted Successfully",
            }, status=status.HTTP_200_OK)


class CRUDStudent(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''Used to get all students created by user'''
        studnets = Student.objects.filter(created_by=request.user)
        return Response({
            "studnets": StudentSerializer(studnets, many=True).data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''Used to create a new course'''
        student_id = request.data.get("student_id")
        student_name = request.data.get("student_name")
        student_level = request.data.get("student_level")
        obj = Student.objects.create(
            student_id=student_id,
            student_name=student_name,
            student_level=student_level,
            created_by=request.user
        )
        return Response({
            "message": "Student Created Successfully",
            "student": StudentSerializer(obj).data
        }, status=status.HTTP_201_CREATED)
        
        
    def put(self, request,*args, **kwargs):
        '''Used to update a course'''
        user = request.user
        student_pk = request.data.get("student_pk") # primary key
        student_id = request.data.get("student_id")
        student_name = request.data.get("student_name")
        student_level = request.data.get("student_level")
        obj = Student.objects.filter(id=student_pk, created_by=user).first()
        # check of course exists
        if obj is None:
            return Response({
                "message": "Student Not Found"
            }, status=status.HTTP_404_NOT_FOUND)
        # check if course belongs to user
        obj.student_id = student_id
        obj.student_name = student_name
        obj.student_level = student_level
        obj.save()
        return Response({
            "message": "Student Updated Successfully",
            "student": StudentSerializer(obj).data
        }, status=status.HTTP_200_OK)
        
    def delete(self, request, *args, **kwargs):
        '''Used to delete a course'''
        user = request.user
        course_id = request.data.get("course_id")
        obj = Course.objects.filter(id=course_id, lecturer=user).first()
        # check of course exists
        if obj is None:
            return Response({
                "message": "Course Fot Found"
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            obj.delete()
            return Response({
                "message": "Course Deleted Successfully",
            }, status=status.HTTP_200_OK)
