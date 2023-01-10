from django.urls import path 

from .views import (AccountDetailView, AccountListView, AccountCreateView,
 AccountUpdateView, AccountDeleteView, AccountSearchView)
from transactions.views import TransactionCreateView 

app_name = "accts"

urlpatterns = [
    path('', AccountListView.as_view(), name="list"),
    path('search/', AccountSearchView.as_view(), name="search"),
    path('create/', AccountCreateView.as_view(), name="create"),
    path('<int:pk>/', AccountDetailView.as_view(), name="detail"),
    path('<int:pk>/update/', AccountUpdateView.as_view(), name="update"),
    path('<int:pk>/delete/', AccountDeleteView.as_view(), name="delete"),
    path('<int:pk>/payment/', TransactionCreateView.as_view(), name="payment")
]