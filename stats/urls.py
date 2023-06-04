from django.urls import path
from .views import UserActivityListView

app_name = "stats"

urlpatterns = [
    path('user-activity/', UserActivityListView.as_view(), name='activity_list'),
]
