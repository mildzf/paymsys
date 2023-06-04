from django.utils import timezone
from ..models import UserActivity

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log user activity
        if request.user.is_authenticated:
            activity = UserActivity.objects.create(
                user=request.user,
                model_name=request.resolver_match.app_name + '.' + request.resolver_match.url_name,
                action_time=timezone.now(),
                is_staff=request.user.is_staff,
            )

        return response
