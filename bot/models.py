from django.db import models
from ckeditor.fields import RichTextField


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(verbose_name="Telegram ID", unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.telegram_id)


class Media(models.Model):
    class MediaType(models.TextChoices):
        file = "file", "File"
        image = "image", "Image"

    file = models.FileField(upload_to="uploads")
    media_type = models.CharField(choices=MediaType.choices, max_length=10)
    notification = models.ForeignKey("Notification", null=True, blank=True, on_delete=models.SET_NULL)


class Notification(models.Model):
    receivers = models.ManyToManyField(TelegramUser, related_name="notifications")
    send_all = models.BooleanField(default=False)
    message = RichTextField(null=True, blank=True)

    @staticmethod
    def send_message(users: TelegramUser, send_all: bool = False) -> None:
        pass
