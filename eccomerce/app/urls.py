from django.urls import path, include
from .views import CustomUserViewSet, LoginView, CategoryViewSet, ProductViewSet, BasketViewSet
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authentication import SessionAuthentication

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'Products', ProductViewSet, basename='Products')
router.register(r'Categorys', CategoryViewSet, basename='Categorys')
router.register(r'Baskets', BasketViewSet, basename='Baskets')

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="Test API with JWT auth",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[SessionAuthentication],
)

urlpatterns = [
    path("", include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('login/', LoginView.as_view(), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
