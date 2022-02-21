from django.apps import AppConfig


class PensionUserNotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pension_user_notification'

    def ready(self):
        import pension_user_notification.signals