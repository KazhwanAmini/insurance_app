from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Insurance API",
        default_version='v1',
        description="API documentation for the Insurance App",
        contact=openapi.Contact(email="your@email.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],  # don't enforce auth on docs
)

from rest_framework_simplejwt.views import  TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('insurance.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('insurance.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

