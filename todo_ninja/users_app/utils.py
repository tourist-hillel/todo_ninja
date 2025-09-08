from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

def create_custom_permissions():
    content_type = ContentType.objects.get_for_model(apps.get_model('users_app', 'ToDoUser'))
    content_type_global, _ = ContentType.objects.get_or_create(app_label='users_app', model='global')

    Permission.objects.get_or_create(
        codename='can_manage_user_permissions',
        name='Може керувати дозволами користувачів',
        content_type=content_type
    )

    Permission.objects.get_or_create(
        codename='global_can_manage_user_permissions',
        name='Може керувати дозволами користувачів(глобальний доступ)',
        content_type=content_type_global
    )
