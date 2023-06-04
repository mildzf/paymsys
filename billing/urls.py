from django.urls import path

from .views import BillView

app_name="billing"

urlpatterns = [
    path("new/", BillView.as_view(), name="create"),


]