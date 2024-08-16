from django.contrib import admin
from student.models import StudentTask, StudentAnswer, RequestsToJoinGroup
from course.models import QuestionSet
from bot.models import TelegramUser

admin.site.register(StudentTask)


class QuestionSetFilter(admin.SimpleListFilter):
    title = 'Question set'
    parameter_name = 'question_set'

    def lookups(self, request, model_admin):
        question_sets = [(question_set.id, question_set.title) for question_set in QuestionSet.objects.all().order_by("-id")]
        return question_sets

    def queryset(self, request, queryset):
        """
        Filters the queryset based on the value provided by the user.
        """
        if self.value():
            return queryset.filter(question__question_set_id=self.value())
        return queryset


class StudentFilter(admin.SimpleListFilter):
    title = 'Student'
    parameter_name = 'student'

    def lookups(self, request, model_admin):
        students = [(student.id, student.first_name) for student in TelegramUser.objects.all().order_by("-id")]
        return students

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(student=self.value())
        return queryset


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ("student", "question", "body", "is_correct", "is_checked")
    list_filter = (QuestionSetFilter, StudentFilter)
    list_editable = ("is_correct", "is_checked")
