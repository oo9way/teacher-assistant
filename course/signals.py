from django.db.models.signals import post_save
from django.dispatch import receiver
from course.models import Task
from student.models import StudentTask


@receiver(post_save, sender=Task)
def create_student_task(sender, instance, created, **kwargs):
    if created:
        groups = instance.lesson.groups.all()
        student_tasks = []
        for group in groups:
            for student in group.members.all():
                student_tasks.append(StudentTask(student=student, task=instance))
        StudentTask.objects.bulk_create(student_tasks)
