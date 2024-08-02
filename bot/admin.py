from django.contrib import admin
from solo.admin import SingletonModelAdmin
from bot import models


class PhotoInline(admin.TabularInline):
    model = models.Photo
    extra = 0
    fields = ("image", )


class SingleAdmin(SingletonModelAdmin):
    fields = ("body", )
    inlines = (PhotoInline, )


admin.site.register(models.Contact, SingleAdmin)
admin.site.register(models.Promotion, SingleAdmin)
admin.site.register(models.Rule, SingleAdmin)
admin.site.register(models.About, SingleAdmin)
admin.site.register(models.Certificate, SingleAdmin)
admin.site.register(models.Social, SingleAdmin)