from django.urls import path, include
from .views import CustomUserViewSet
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="Test API with JWT auth",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[SessionAuthentication],  # Add JWTAuthentication if you use JWT
)


urlpatterns = [
    path("", include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]