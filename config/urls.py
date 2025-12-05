from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.conf import settings


urlpatterns = [
    # Health check / home
    path("", include("apps.core.urls")),
    # Admin
    path("admin/", admin.site.urls),
    # API endpoints
    path("api/users/", include("apps.users.urls")),
    path("api/events/", include("apps.events.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        # API Documentation
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/docs/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
        ),
    ]
