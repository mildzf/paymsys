from django.urls import path 

from .views import InvoiceDetailView 

app_name="billing"

urlpatterns = [
    path("<int:pk>/", InvoiceDetailView.as_view(), name="detail"),
]