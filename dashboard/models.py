import uuid

from django.db import models
from django.utils import timezone
from samples.models import UserMachineModel


class ExperimentChoices(models.TextChoices):
    SEM = 'sem', 'SEM'
    TEM = 'tem', 'TEM'
    XRD = 'xrd', 'XRD'
    AFM = 'afm', 'AFM'
    APT = 'apt', 'APT'
    MBE = 'mbe', 'MBE'
    CVD = 'cvd', 'CVD'


class Meeting(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    participants = models.ManyToManyField(UserMachineModel)
    date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    participants = models.ManyToManyField(UserMachineModel)

    def __str__(self):
        return self.title


class Machine(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    users = models.ManyToManyField(UserMachineModel)
    experiment = models.CharField(
        max_length=10,
        choices=ExperimentChoices.choices,
    )

    def __str__(self):
        return self.name + " (" + self.location + ")"
