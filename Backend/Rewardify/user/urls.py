from django.urls import path
from .views import UserProfileAPIView, UserPointsView, get_apps, SubmitTaskView, UserPointsSummaryAPIView

urlpatterns = [
    path("user-profile/", UserProfileAPIView.as_view(), name="user-profile"),
    path("user-points/", UserPointsView.as_view(), name="user-points"),
    path("user-apps/", get_apps, name="get_apps"),
    path('submit-task/', SubmitTaskView.as_view(), name='submit-task'),
    path('user-points-summary/', UserPointsSummaryAPIView.as_view(), name='user-points-summary'),
]
