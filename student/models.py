from django.db import models
from course import models as course_models
from bot.models import TelegramUser
from group.models import Group


class StudentTask(models.Model):
    student: TelegramUser = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    task: course_models.Task = models.ForeignKey(course_models.Task, on_delete=models.CASCADE)
    body = models.TextField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.first_name


class StudentAnswer(models.Model):
    student: TelegramUser = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    question: course_models.Question = models.ForeignKey(course_models.Question, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.student.first_name


class RequestsToJoinGroup(models.Model):
    student: TelegramUser = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    group: Group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.first_name} - {self.group.name}"
