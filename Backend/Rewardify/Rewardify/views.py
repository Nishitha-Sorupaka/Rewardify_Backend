from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator

from user.models import *

def index(request):
    return render(request, "index.html")

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate input
        if not email or not password:
            return JsonResponse({"error": "Email and password are required"}, status=400)

        user = authenticate(username=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)

            response_data = {
                "message": "Login successful",
                "redirect_url": "",
                "token": str(refresh.access_token),
            }

            # Redirect based on user role
             if user.is_superuser:
                response_data["redirect_url"] = "https://nishitha-sorupaka.github.io/Rewardify/adminhome.html"
            elif user.is_authenticated:
                response_data["redirect_url"] = "https://nishitha-sorupaka.github.io/Rewardify/userprofile.html"


            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({"error": "Invalid email or password"}, status=401)

User = get_user_model()

class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:    
            full_name = request.data.get('name')
            email = request.data.get('email')
            password = request.data.get('password')
            confirm_password = request.data.get('confirmPassword')

            if password != confirm_password:
                return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=email).exists():
                return Response({"error": "Email is already registered."}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = full_name
            user.save()

            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def add_app(request):

    data = request.data
    try:
        app = App(
            name=data.get('name'),
            link=data.get('link'),
            category=data.get('category'),
            subcategory=data.get('subcategory'),
            points=data.get('points')
        )
        app.full_clean()  
        app.save()  
        return Response({'message': 'App added successfully!'}, status=201)
    except ValidationError as e:
        return Response({'error': str(e)}, status=400)
    except Exception as e:
        return Response({'error': 'An error occurred while saving the app.'}, status=500)
    
def list_apps(request):
    apps = App.objects.order_by('-created_at')
    app_list = [
        {
            "name": app.name,
            "link": app.link,
            "category": app.category,
            "subcategory": app.subcategory,
            "points": app.points,
            "status": app.App_status,
            "created_at": app.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": app.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for app in apps
    ]
    return JsonResponse(app_list, safe=False)


def list_users(request):
    users = User.objects.all()
    user_list = [
        {
            "username": user.username,
            "email": user.email,
            "status": user.is_active,
            "date_joined": user.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for user in users
    ]
    return JsonResponse(user_list, safe=False)

class AdminDashboardStatsAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        total_users = CustomUser.objects.filter(is_user=True).count()

        total_apps = App.objects.count()
        total_users_submitted_task = UserPoints.objects.values('user').distinct().count()

        return Response({
            "total_users": total_users,
            "total_apps": total_apps,
            "total_users_submitted_task": total_users_submitted_task
        }, status=200)
