from __future__ import unicode_literals
import csv

from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from ckeditor_uploader.fields import RichTextUploadingField
from groupsystem.models import BasicGroup

# Create your models here.


def random_string():
    return get_random_string(length=6)


class EmailGroup(models.Model):
    name = models.CharField(max_length=200, verbose_name='List Name')
    users = models.ManyToManyField(
        User,
        verbose_name='Select from List',
        blank=True,
        related_name='emailgroups'
    )
    csv_file = models.FileField(
        verbose_name='CSV Upload List',
        upload_to='csvs',
        null=True,
        blank=True
    )
    basic_group = models.OneToOneField(
        BasicGroup,
        verbose_name='Link to Group',
        null=True,
        blank=True
    )

    def __unicode__(self):
        return self.name


class EmailId(models.Model):
    emailgroup = models.ForeignKey(EmailGroup, related_name='emailids')
    first_name = models.CharField(max_length=100, default='', blank=True)
    last_name = models.CharField(max_length=100, default='', blank=True)
    user = models.ForeignKey(User, null=True)
    email_id = models.EmailField(null=True)
    send_email_from_group = models.BooleanField(default=True)
    send_email_from_ekata = models.BooleanField(default=True)

    def __unicode__(self):
        if self.first_name or self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return self.email_id


class EmailTemplate(models.Model):
    name = models.CharField(max_length=300, blank=False)
    html_file = models.FileField(upload_to='emailtemplates', null=True, blank=True)
    template = RichTextUploadingField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class EmailCampaign(models.Model):
    campaign_name = models.CharField(max_length=300, blank=False)
    template = models.ForeignKey(EmailTemplate)
    subject = models.CharField(max_length=100)
    message = RichTextUploadingField()
    timestamp = models.DateTimeField(auto_now_add=True)
    draft = models.BooleanField(default=True)
    tracking_id = models.CharField(default=random_string, editable=False, max_length=10)

    def __unicode__(self):
        return self.campaign_name


class CampaignTracking(models.Model):
    campaign = models.ForeignKey(EmailCampaign, related_name='trackings')
    emailid = models.EmailField(null=True)
    sent = models.BooleanField(default=False)
    opened = models.BooleanField(default=False)
    opened_at = models.DateTimeField(null=True, blank=True)
    tracking_id = models.CharField(default=random_string, editable=False, max_length=10)


def save_emailids_from_csv(sender, instance, **kwargs):
    if instance.csv_file:
        csv_f = open(instance.csv_file.path, 'r')
        email_infos = csv.reader(csv_f)
        for email_info in email_infos:
            emailid, created = EmailId.objects.get_or_create(
                emailgroup=instance,
                first_name=email_info[0],
                last_name=email_info[1],
                email_id=email_info[2]
            )
            emailid.save()
        csv_f.close()


def save_emailids_from_siteusers(sender, instance, **kwargs):
    action = kwargs.pop('action', None)
    if action == 'post_add':
        pk_set = kwargs.pop('pk_set', None)
        for pk in pk_set:
            user = User.objects.get(id=pk)
            if user.email:
                emailid, created = EmailId.objects.get_or_create(
                    emailgroup=instance,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email_id=user.email
                )
                emailid.save()


def populate_template(sender, instance, **kwargs):
    if instance.html_file and not instance.template:
        html_file = open(instance.html_file.path, 'r')
        html = html_file.read()
        instance.template = html
        html_file.close()
        instance.save()


post_save.connect(save_emailids_from_csv, sender=EmailGroup)
m2m_changed.connect(
    save_emailids_from_siteusers,
    sender=EmailGroup.users.through
)
post_save.connect(populate_template, sender=EmailTemplate)
