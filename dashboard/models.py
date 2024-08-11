import uuid

from django.db import models
from django.utils import timezone
from samples.models import UserMachineModel


class Meeting(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    participants = models.ManyToManyField(UserMachineModel)
    date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.title
