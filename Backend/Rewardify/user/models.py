from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_user = models.BooleanField(default=True)

class App(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    category = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255)
    points = models.PositiveIntegerField(default=0)
    App_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.category} ({self.subcategory})"

class UserPoints(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="earned_points")
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name="tasks")
    points_earned = models.PositiveIntegerField(default=0)
    screenshot = models.ImageField(upload_to="task_screenshots/", blank=True, null=True)  

    def __str__(self):
        return f"{self.user.username} earned {self.points_earned} points for {self.app.name}"