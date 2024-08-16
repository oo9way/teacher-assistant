from django.contrib import admin
from django.urls import path
from bot.views import webhook
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("telegram/", webhook.urls),
    path('', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
