from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self) -> None:
        import app.signals.film_signals
        import app.signals.user_signals
        import app.signals.review_signals