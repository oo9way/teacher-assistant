from django.contrib import admin
from course import models


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title",)


@admin.register(models.Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "created_at", "updated_at")
    search_fields = ("title", "course__title")


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "created_at", "updated_at")
    search_fields = ("title", "course__title")


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("body", "lesson",)
    search_fields = ("body", "lesson__name",)


class QuestionInline(admin.TabularInline):
    model = models.Question
    extra = 0


@admin.register(models.QuestionSet)
class QuestionSetAdmin(admin.ModelAdmin):
    list_display = ("title", "lesson",)
    search_fields = ("title", "lesson__title")
    inlines = [QuestionInline]
