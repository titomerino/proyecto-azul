from django.apps import AppConfig


class OutputConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'output'
    verbose_name = "Egreso"
    verbose_name_plurar = "Egresos"
