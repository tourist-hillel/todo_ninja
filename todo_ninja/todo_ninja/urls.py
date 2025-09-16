"""
URL configuration for todo_ninja project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
# from ninja import NinjaAPI
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from ws_chat.views import register
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from todo_ninja.debug_view import debug_session

# from api.views import router as task_router

# api = NinjaAPI(
#     title='ToDo API',
#     description='A simple ToDo API built with django-ninja',
#     version='1.0.0',
#     docs_url='/docs/'
# )

# api.add_router('task_api', task_router)
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', api.urls),
    path('permissions/', include('users_app.urls')),
    path('', include('books.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('mixins/', include('mixins_example.urls')),
    path('drf_api/', include('lib_drf.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='obtain_token_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('chat/', include('ws_chat.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('register/', register, name='register'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
    path('debug-session/', debug_session, name='debug_session'),
]
