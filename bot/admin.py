from bot.models import TelegramUser, Notification, Media
from django.contrib import admin
from bot.tasks import send_notification as send_notification_task
from django.utils.safestring import mark_safe


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "first_name", "last_name", "phone_number")
    search_fields = ("first_name", "last_name", "telegram_id")


class MediaInline(admin.TabularInline):
    model = Media
    extra = 0


def send_notification(modeladmin, request, queryset):
    notification_ids = queryset.values_list("id", flat=True)
    send_notification_task.delay(notification_ids)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "get_notification_display", "send_all",)
    search_fields = ("receivers", "media", "message")
    fields = ("receivers", "send_all", "message")
    autocomplete_fields = ("receivers",)
    inlines = (MediaInline,)

    def get_notification_display(self, obj):
        return mark_safe(obj.message)
