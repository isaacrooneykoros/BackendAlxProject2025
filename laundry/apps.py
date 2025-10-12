from django.apps import AppConfig


class LaundryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'laundry'

    def ready(self):
        import laundry.signals  # 👈 ensures signals are loaded
