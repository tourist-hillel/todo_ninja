from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lib_drf.views import AuthorViewSet, BookViewSet, ObtainAuthToken
from lib_drf.auth import ObtainJWT, RefreshJWT


router_drf = DefaultRouter()
router_drf.register(r'authors', AuthorViewSet, basename='author')
router_drf.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router_drf.urls)),
    path('obtain_token/', ObtainJWT.as_view(), name='obtain-token'),
    path('refresh_token/', RefreshJWT.as_view(), name='refresh-token'),
]