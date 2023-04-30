from django.db import models

from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=1024)
    status = models.ForeignKey('statuses.status', on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='author')
    executor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='executor')
    created_at = models.DateTimeField(auto_now_add=True)
