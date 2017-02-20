from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Contact(models.Model):
    first_name = models.CharField(verbose_name=_('First Name'), max_length=200)
    last_name = models.CharField(verbose_name=_('Last Name'), max_length=200)
    company_name = models.CharField(
        verbose_name=_('Company Name'), max_length=200, default='', blank=True)
    email_address = models.EmailField(verbose_name=_('Email Address'), )
    telephone_no = models.CharField(
        verbose_name=_('Telephone Number'),
        max_length=20, default='', blank=True)
    comment = models.TextField(
        verbose_name=_('Comment'), default='', blank=True)

    def __unicode__(self):
        return self.first_name + self.last_name
