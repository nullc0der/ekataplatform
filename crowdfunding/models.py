from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.


class CrowdFund(models.Model):
    goal = models.PositiveIntegerField(
        null=True, blank=True
    )
    raised = models.PositiveIntegerField(
        null=True, blank=True
    )
    active = models.BooleanField(default=False)

    class Meta:
        get_latest_by = 'id'
