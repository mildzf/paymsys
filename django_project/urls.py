from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import private_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("private/", include(private_urls)),
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
