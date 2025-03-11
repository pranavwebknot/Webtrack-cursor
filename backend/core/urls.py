from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="WebTrack API",
        default_version='v1',
        description="API documentation for WebTrack",
        terms_of_service="https://www.webtrack.com/terms/",
        contact=openapi.Contact(email="contact@webtrack.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('webtrack_tracking.urls')),
    path('api/', include('webtrack_analytics.urls')),
    path('api/', include('webtrack_notifications.urls')),
    path('api/', include('webtrack_reports.urls')),
    path('api/', include('webtrack_settings.urls')),
    path('api/', include('webtrack_integrations.urls')),
    path('api/', include('webtrack_audit.urls')),
    path('api/', include('webtrack_feedback.urls')),
    path('api/', include('webtrack_help.urls')),
    path('api/', include('webtrack_api.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
