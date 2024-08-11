from django.db import models
from course import models as course_models
from bot.models import TelegramUser


class Group(models.Model):
    course: course_models.Course = models.ForeignKey(course_models.Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    finished_lessons = models.ManyToManyField(course_models.Lesson, related_name='groups', null=True, blank=True)
    members = models.ManyToManyField(TelegramUser, related_name='groups', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name