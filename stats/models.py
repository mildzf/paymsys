from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=255)
    action_time = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    class Meta:
        ordering = ('-action_time',)
