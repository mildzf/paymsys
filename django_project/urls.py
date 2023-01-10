from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("clients/", include("clients.urls", namespace="clients")), 
    path("accts/", include("accts.urls", namespace="accts")),
    path("transactions/", include("transactions.urls", namespace="transactions")),
    path("invoice/", include("billing.urls", namespace="billing")),
    path("", include("pages.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
