from django.urls import path

from .views import DashboardView, AboutPageView, SearchView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path("about/", AboutPageView.as_view(), name="about"),
    path("search", SearchView.as_view(), name="search"),
]
