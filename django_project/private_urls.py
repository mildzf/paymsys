from django.urls import include, path 


urlpatterns = [
    path("clients/", include("clients.urls", namespace="clients")), 
    path("accts/", include("accts.urls", namespace="accts")),
    path("transactions/", include("transactions.urls", namespace="transactions")),
    path("billing/", include("billing.urls", namespace="billing")),
    path("tasks/", include("tasks.urls", namespace="tasks")),
    path("", include("pages.urls")),
]