from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from group.models import Group
from student.models import StudentTask
from course.models import Task


@receiver(m2m_changed, sender=Group.members.through)
def create_student_tasks(sender, instance, action, **kwargs):
    if action == "post_add":
        for student in instance.members.all():
            for task in Task.objects.all():
                try:
                    StudentTask.objects.get_or_create(student=student, task=task)
                except:
                    pass