from django.apps import AppConfig


class GroupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'group'

    def ready(self):
        from group.signals import create_student_tasks