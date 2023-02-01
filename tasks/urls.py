from django.urls import path 
from django.views.generic import TemplateView

from .views import charge_accounts 


app_name="tasks"

urlpatterns = [
    path("all/", TemplateView.as_view(template_name="tasks/index.html"), name="index"),
    path("charge/", charge_accounts, name="charge")
]