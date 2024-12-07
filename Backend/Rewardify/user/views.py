from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.views import View
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from user.models import *

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        data = {
            "email": user.email,
            "first_name": user.first_name,
            "date_joined": user.date_joined.strftime('%Y-%m-%d'),
        }
        return Response(data, status=200)


class UserPointsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        available_tasks = App.objects.filter(App_status=True)  
        user_points = UserPoints.objects.filter(user=user)
        points_data = [
            {
                "app_id": point.app.id,
                "app_name": point.app.name,
                "points_earned": point.points_earned,
            }
            for point in user_points
        ] if user_points.exists() else []

        tasks_data = [
            {
                "id": task.id,
                "name": task.name,
                "category": task.category,
                "subcategory": task.subcategory,
                "points": task.points,
            }
            for task in available_tasks
        ]

        response_data = {
            "available_tasks": tasks_data,
            "user_points": points_data,
        }

        return JsonResponse(response_data)


def get_apps(request):
    apps = App.objects.all()
    
    app_list = [
        {
            "id": app.id,
            "name": app.name,
            "link": app.link,
            "points": app.points,
            "category": app.category
        }
        for app in apps
    ]
    return JsonResponse(app_list, safe=False)

import logging

logger = logging.getLogger(__name__)

class SubmitTaskView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        app_id = request.data.get('app_id')
        screenshot = request.FILES.get('screenshot')

        if not app_id or not screenshot:
            return Response({"error": "App ID and screenshot are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            app = App.objects.get(id=app_id)
        except App.DoesNotExist:
            return Response({"error": "App not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            user_task = UserPoints.objects.create(
                user=user, app=app, screenshot=screenshot, points_earned=app.points
            )
            user_task.save()
            logger.info(f"Task submitted successfully for user {user.username} and app {app.name}.")
            return Response({"message": "Task submitted successfully!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error saving task for user {user.username}: {e}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserPointsSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        user_tasks = UserPoints.objects.filter(user=user)

        total_points = user_tasks.aggregate(total=models.Sum('points_earned'))['total'] or 0

        points_data = {
            "user": user.username,
            "total_points": total_points,
            "tasks": [
                {
                    "app_name": task.app.name,
                    "points_earned": task.points_earned,
                    "category": task.app.category,
                    "app_logo": task.app.link, 
                }
                for task in user_tasks
            ],
        }
        return Response(points_data, status=200)