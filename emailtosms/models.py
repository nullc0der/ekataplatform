from __future__ import unicode_literals

import csv

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from invitationsystem.models import random_string
# Create your models here.


class CarrierCSV(models.Model):
    name = models.CharField(max_length=40)
    csv = models.FileField(upload_to='carriercsvs')

    def __unicode__(self):
        return self.name


class Carrier(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    emailaddress = models.EmailField(null=True)
    verified = models.BooleanField(default=False, editable=False)
    verified_times = models.IntegerField(default=0, editable=False)

    def __unicode__(self):
        if self.emailaddress:
            domain = self.emailaddress.split('@')
            return self.country + ' ' + self.name + ' ' + '@' + domain[1]
        else:
            return self.country + ' ' + self.name


class Verifier(models.Model):
    user = models.ForeignKey(User, related_name='carriers_verified')
    carrier = models.ForeignKey(Carrier)
    code = models.CharField(max_length=10, default=random_string)


def save_carrier_from_csv(sender, instance, **kwargs):
    if instance.csv:
        csv_f = open(instance.csv.path, 'r')
        carriers_info = csv.reader(csv_f)
        for carrier_info in carriers_info:
            carrier, created = Carrier.objects.get_or_create(
                name=carrier_info[2],
                country=carrier_info[0],
                emailaddress=carrier_info[4]
            )
            carrier.save()
        csv_f.close()

post_save.connect(save_carrier_from_csv, sender=CarrierCSV)


class UserCarrier(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    emailaddress = models.EmailField(null=True, blank=True)
    added_to_carrier = models.BooleanField(default=False, editable=False)

    class Meta:
        verbose_name = 'User requested carrier'

    def __unicode__(self):
        return self.name + ' ' + self.country
