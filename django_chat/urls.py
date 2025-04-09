# django_chat/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Define the schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Django Chat API",
        default_version='v1',
        description="API documentation for the Django chat app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@django-chat.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chat.urls')),  # Add your app's URL routing here
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),  # Swagger UI
]
