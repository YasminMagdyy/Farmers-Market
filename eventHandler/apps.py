from django.apps import AppConfig


class EventhandlerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eventHandler'
    
    def ready(self):
        # This will load the signal handlers
        import eventHandler.event_handlers  # noqa
