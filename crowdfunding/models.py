from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.


class CrowdFund(models.Model):
    goal = models.DecimalField(
        max_digits=30, decimal_places=2, validators=[MinValueValidator(1.00)]
    )
    raised = models.DecimalField(
        null=True, blank=True, max_digits=30, decimal_places=2, default=0.00
    )
    active = models.BooleanField(default=False)

    class Meta:
        get_latest_by = 'id'
