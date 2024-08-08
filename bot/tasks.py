from celery import shared_task
from bot.models import Notification


@shared_task
def send_notification(notification_ids: list[int]):
    notifications = Notification.objects.filter(id__in=notification_ids)

    for notification in notifications:
        notification.send_message(notification.receivers.all(), notification.send_all)
