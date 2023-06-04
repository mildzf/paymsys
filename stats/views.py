from django.views.generic import ListView
from .models import UserActivity

class UserActivityListView(ListView):
    model = UserActivity
    template_name = 'stats/user_activity_list.html'
    paginate_by = 20
