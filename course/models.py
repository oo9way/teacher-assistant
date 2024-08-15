from django.db import models
from bot.models import TelegramUser

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Module(models.Model):
    course: Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    module: Module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class QuestionSet(models.Model):
    lesson: Lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="questions")
    title = models.CharField(max_length=255)
    answered_students = models.ManyToManyField(TelegramUser, related_name="answered_question_sets", blank=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    question_set: QuestionSet = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, null=True, blank=True, related_name="questions")
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Task(models.Model):
    lesson: Lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="tasks")
    body = models.TextField()

    def __str__(self):
        return self.lesson.title