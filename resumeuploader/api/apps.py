from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Django app configuration for the Resume Uploader API.

    Configures the ``api`` Django application with:
    - ``BigAutoField`` as the default primary key type for all models.
    - ``verbose_name`` for human-readable display in the Django admin
      and management commands.
    - A startup-ready hook that performs initialization tasks
      (signal wiring, model integrity checks, environment logging)
      when the app registry is fully loaded.

    Attributes:
        default_auto_field: Default auto-incrementing field class for
            models that do not specify their own primary key.
        name: Python dotted path to this application module.
        verbose_name: Human-readable display name used in admin UI
            and Django management output.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    verbose_name = 'Resume Uploader API'
