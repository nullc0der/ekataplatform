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
    default_note = models.CharField(
        default='', max_length=200, blank=True,
        help_text=_('set a default note for the payment form')
    )
    thankyou_message = models.TextField(
        default=_('Thank You'), blank=True,
        help_text=_('Customize the payment form thank you message')
    )
    introduction = models.TextField(
        default='', blank=True,
        help_text=_('Write a introduction')
    )
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=False)
    cards_html = models.TextField(default='', blank=True)
    admin_cards_html = models.TextField(default='', blank=True)

    class Meta:
        get_latest_by = 'id'


class PredefinedAmount(models.Model):
    crowdfund = models.ForeignKey(CrowdFund)
    amount = models.PositiveIntegerField()
    default = models.BooleanField(default=False)


class ProductFeature(models.Model):
    crowdfund = models.ForeignKey(CrowdFund)
    name = models.CharField(max_length=100, default='', blank=False)
    fa_icon_name = models.CharField(
        default='cog', max_length=40, blank=True,
        help_text=_('Add font Awesome icon name here')
    )
    fa_icon_color = models.CharField(
        default='#9F9F9F', max_length=7, blank=True
    )


class HeaderVideo(models.Model):
    crowdfund = models.ForeignKey(CrowdFund)
    video = models.FileField(upload_to='crowdfund_header_videos')

    class Meta:
        get_latest_by = 'id'
