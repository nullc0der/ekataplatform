from __future__ import unicode_literals
import csv

from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.


class EmailGroup(models.Model):
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(
        User,
        verbose_name='Site user',
        blank=True,
        related_name='emailgroups'
    )
    csv_file = models.FileField(upload_to='csvs', null=True, blank=True)

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
    template = RichTextUploadingField()

    def __unicode__(self):
        return self.name


class EmailCampaign(models.Model):
    FROM_EMAIL_CHOICES = (
        ('support@ekata.social', 'support@ekata.social'),
        ('news@ekata.social', 'news@ekata.social'),
        ('newsletter@ekata.social', 'newsletter@ekata.social'),
    )
    campaign_name = models.CharField(max_length=300, blank=False)
    template = models.OneToOneField(EmailTemplate)
    to_groups = models.ManyToManyField(EmailGroup)
    subject = models.CharField(max_length=100)
    message = RichTextUploadingField()
    from_email = models.EmailField(
        default='support@ekata.social',
        choices=FROM_EMAIL_CHOICES
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.campaign_name


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

post_save.connect(save_emailids_from_csv, sender=EmailGroup)
m2m_changed.connect(
    save_emailids_from_siteusers,
    sender=EmailGroup.users.through
)
