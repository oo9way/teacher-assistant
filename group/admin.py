from django.contrib import admin
from group import models


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "created_at", "updated_at")
    search_fields = ("name", "course__title")
