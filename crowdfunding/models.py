from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class CrowdFund(models.Model):
    goal = models.PositiveIntegerField(
        null=True, blank=True
    )
    raised = models.PositiveIntegerField(
        null=True, blank=True
    )
    active = models.BooleanField(default=False)
    default_note = models.CharField(
        default='', max_length=200, blank=True,
        help_text=_('set a default note for the payment form')
    )

    class Meta:
        get_latest_by = 'id'


class PredefinedAmount(models.Model):
    crowdfund = models.ForeignKey(CrowdFund)
    amount = models.PositiveIntegerField()
    default = models.BooleanField(default=False)
