from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_permissions(sender, **kwargs):
    from users_app.utils import create_custom_permissions
    create_custom_permissions()

class UsersAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users_app'

    def ready(self):
        post_migrate.connect(create_permissions, sender=self)
