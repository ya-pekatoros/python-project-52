from django.db import models

from django.contrib.auth.models import User

from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=1024)
    status = models.ForeignKey('statuses.status', on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='author')
    executor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='executor')
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(
        Label,
        through='TasksLabels',
        through_fields=('task', 'label'),
        blank=True
    )


class TasksLabels(models.Model):
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
