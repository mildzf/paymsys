from django.urls import path 

from .views import (TransactionCreateView, TransactionDetailView, 
TransactionListView,  receipt)


app_name="transactions"

urlpatterns = [
    path('', TransactionListView.as_view(), name='list'),
    path('new/', TransactionCreateView.as_view(), name='create'),
    path('<int:pk>/', TransactionDetailView.as_view(), name='detail'),
    path('<int:pk>/receipt/', receipt, name="receipt"),
    
]