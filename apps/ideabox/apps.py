from django.apps import AppConfig


class IdeaboxConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ideabox'
    
    def ready(self):
        import apps.ideabox.signals
