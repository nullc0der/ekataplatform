from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(User, related_name='payments')
    amount = models.DecimalField(
        null=True, blank=True, max_digits=30, decimal_places=2
    )
    is_success = models.BooleanField(default=False)
    message = models.CharField(default='', max_length=250)
    payment_type = models.CharField(default='', max_length=100)
    fail_reason = models.CharField(default='', max_length=300)
    charge_id = models.CharField(default='', max_length=200)
    date = models.DateField(auto_now_add=True, null=True)

#  TODO: Subscription model, possible attribute: plan, customer_id, user
#  TODO: Customer model, possible attribute: customer_id, user
