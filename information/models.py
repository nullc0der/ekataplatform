from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Contact(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, default='', blank=True)
    email_address = models.EmailField()
    telephone_no = models.CharField(max_length=20, default='', blank=True)
    comment = models.TextField(default='', blank=True)

    def __unicode__(self):
        return self.first_name + self.last_name
