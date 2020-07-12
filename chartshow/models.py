from datetime import datetime
from random import Random

from django.db import models


class Owner(models.Model):
    owner_id = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)

    def __str__(self):  # __unicode__ on Python 2
        return self.owner


class WorkList(models.Model):
    row_id = models.CharField(max_length=200, unique=True)
    owner = models.CharField(max_length=100)
    mid = models.CharField(max_length=50)
    bug = models.CharField(max_length=50, null=True)
    procedure = models.CharField(max_length=200)
    room = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    progress = models.CharField(max_length=50, null=True)
    hours = models.CharField(max_length=50, null=True)
    progress_delta = models.CharField(max_length=50, null=True)
    hours_delta = models.CharField(max_length=50, null=True)
    modified_at = models.DateField()

    def __str__(self):  # __unicode__ on Python 2
        return self.bug
