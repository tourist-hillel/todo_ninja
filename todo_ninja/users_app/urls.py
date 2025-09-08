from django.urls import path
from users_app.views import manage_user_permissions, check_permission

urlpatterns = [
    path('manage-permissions/', manage_user_permissions, name='manage_user_permissions'),
    path('check-permissions/', check_permission, name='check_permission')
]
