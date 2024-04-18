from django.apps import AppConfig
from django.db.models.signals import post_migrate
from register import create_admin_account


class RegisterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'register'

    def ready(self):
        # Connect the post_migrate signal
        post_migrate.connect(create_admin_account.create_admin_group_and_account, sender=self)
