from django.apps import AppConfig
from django.db.models.signals import post_save


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from .models import UserModel
        from .signals import add_user_to_group
        post_save.connect(add_user_to_group, sender=UserModel)
