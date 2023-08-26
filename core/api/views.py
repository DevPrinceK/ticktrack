from django.shortcuts import render

# import restapi essentials
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response


class OverviewAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({
            "message": "The API for TickTract is running successfully",
            "endpoints": [
                {"endpoint": "/", "description": "returns the overview of the entire api infrastructure"},
            ]
        })
