"""
URL configuration for Rewardify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from Rewardify import views as admins

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('user.urls')),

    path('', admins.index, name='index'),
    path('api/login/', admins.LoginAPIView.as_view(), name='api-login'),
    path('api/signup/', admins.SignupAPIView.as_view(), name='api-signup'),
    path('api/add-app/', admins.add_app, name='add_app'),
    path('api/apps/', admins.list_apps, name='list_apps'),
    path('api/admin-dashboard-stats/', admins.AdminDashboardStatsAPIView.as_view(), name='admin-dashboard-stats'),
    path('api/users/', admins.list_users, name='list_users'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)