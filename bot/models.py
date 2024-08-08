from typing import Any
from django.db import models
from solo.models import SingletonModel
from ckeditor.fields import RichTextField
from utils.cleaner import clean_tags


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(verbose_name="Telegram ID", unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    

class Media(models.Model):
    class MediaType(models.TextChoices):
        file = "file", "File"
        image = "image", "Image"
    
    file = models.FileField(upload_to="uploads")
    media_type = models.CharField(choices=MediaType.choices)


class Notification(models.Model):
    pass




class Photo(models.Model):
    image = models.ImageField(upload_to="gallery")
    promotion = models.ForeignKey("bot.Promotion", null=True, blank=True, related_name="images", on_delete=models.CASCADE)
    contact = models.ForeignKey("bot.Contact", null=True, blank=True, related_name="images", on_delete=models.CASCADE)
    about = models.ForeignKey("bot.About", null=True, blank=True, related_name="images", on_delete=models.CASCADE)
    certificate = models.ForeignKey("bot.Certificate", null=True, blank=True, related_name="images", on_delete=models.CASCADE)
    rule = models.ForeignKey("bot.Rule", null=True, blank=True, related_name="images", on_delete=models.CASCADE)
    social = models.ForeignKey("bot.Social", null=True, blank=True, related_name="images", on_delete=models.CASCADE)


class BaseContentModel(models.Model):
    body = RichTextField(verbose_name="Post matni")

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.body = clean_tags(self.body)
        return super().save(*args, **kwargs)
    
    def send_message(self, chat_id):
        from bot.dispatcher import bot
        
        photos = self.images.all()
        
        if len(photos) == 1:
            return bot.send_photo(chat_id=chat_id, photo=photos.first().image, caption=self.body, parse_mode="html")
        
        elif len(photos) > 1:
            photos = [photo.image for photo in photos]
            return bot.send_media_group(chat_id=chat_id, media=photos, caption=self.body, parse_mode="html")
        
        else:
            return bot.send_message(chat_id=chat_id, text=self.body, parse_mode="html")



    class Meta:
        abstract = True

class Promotion(BaseContentModel, SingletonModel):

    def __str__(self):
        return "Aksiyalar"
    
    class Meta:
        verbose_name = "Aksiya"
        verbose_name_plural = "Aksiya"


class Contact(BaseContentModel, SingletonModel):
    def __str__(self) -> str:
        return "Kontaktlar"
    
    class Meta:
        verbose_name = "Kontaktlar"
        verbose_name_plural = "Kontaktlar"


class Rule(BaseContentModel, SingletonModel):
    def __str__(self) -> str:
        return "Qoidalar"
    
    class Meta:
        verbose_name = "Qoidalar"
        verbose_name_plural = "Qoidalar"


class About(BaseContentModel, SingletonModel):
    def __str__(self) -> str:
        return "Biz haqimizda"
    
    class Meta:
        verbose_name = "Biz haqimizda"
        verbose_name_plural = "Biz haqimizda"


class Certificate(BaseContentModel, SingletonModel):
    def __str__(self) -> str:
        return "Sertifikat"
    
    class Meta:
        verbose_name = "Sertifikatlar"
        verbose_name_plural = "Sertifikatlar"


class Social(BaseContentModel, SingletonModel):
    def __str__(self) -> str:
        return "Ijtimoiy tarmoqlar"
    
    class Meta:
        verbose_name = "Ijtimoiy tarmoqlar"
        verbose_name_plural = "Ijtimoiy tarmoqlar"