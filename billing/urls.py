from django.urls import path 

from .views import InvoicingView

app_name="billing"

urlpatterns = [
    path("new/", InvoicingView.as_view(), name="create"),
    
    
]