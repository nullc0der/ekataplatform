from __future__ import unicode_literals
import os
import random

from django.db import models
from django.dispatch import receiver
from django.core.cache import cache
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.utils.translation import ugettext_lazy as _
from versatileimagefield.fields import VersatileImageField
from jsonfield import JSONField
from django_countries.fields import CountryField

from profilesystem.tasks import task_unique_ekata_id_setter
# Create your models here.


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('1', _('Male')),
        ('2', _('Female')),
        ('3', 'Agender'),
        ('4', 'Androgyne'),
        ('5', 'Androgynous'),
        ('6', 'Bigender'),
        ('7', 'Cis'),
        ('8', 'Cisgender'),
        ('9', 'Cis Female'),
        ('10', 'Cis Male'),
        ('11', 'Cis Man'),
        ('12', 'Cis Woman'),
        ('13', 'Cisgender Female'),
        ('14', 'Cisgender Male'),
        ('15', 'Cisgender Man'),
        ('16', 'Cisgender Woman'),
        ('17', 'Female to Male'),
        ('18', 'FTM'),
        ('19', 'Gender Fluid'),
        ('20', 'Gender Nonconforming'),
        ('21', 'Gender Questioning'),
        ('22', 'Gender Variant'),
        ('23', 'Genderqueer'),
        ('24', 'Intersex'),
        ('25', 'Male to Female'),
        ('26', 'MTF'),
        ('27', 'Neither'),
        ('28', 'Neutrois'),
        ('29', 'Non-binary'),
        ('30', 'Other'),
        ('31', 'Pangender'),
        ('32', 'Trans'),
        ('33', 'Trans*'),
        ('34', 'Trans Female'),
        ('35', 'Trans* Female'),
        ('36', 'Trans Male'),
        ('37', 'Trans* Male'),
        ('38', 'Trans Man'),
        ('39', 'Trans* Man'),
        ('40', 'Trans Person'),
        ('41', 'Trans* Person'),
        ('42', 'Trans Woman'),
        ('43', 'Trans* Woman'),
        ('44', 'Transfeminine'),
        ('45', 'Transfeminine'),
        ('46', 'Transgender'),
        ('47', 'Transgender Female'),
        ('48', 'Transgender Male'),
        ('49', 'Transgender Man'),
        ('50', 'Transgender Person'),
        ('51', 'Transgender Woman'),
        ('52', 'Transmasculine'),
        ('53', 'Transsexual'),
        ('54', 'Transsexual Female'),
        ('55', 'Transsexual Male'),
        ('56', 'Transsexual Man'),
        ('57', 'Transsexual Person'),
        ('58', 'Transsexual Woman'),
        ('59', 'Two-Spirit'),
    )
    user = models.OneToOneField(User, related_name='profile')
    avatar = VersatileImageField(
        verbose_name='user avatar',
        upload_to='avatar',
        null=True,
        blank=True
    )
    default_avatar_color = models.CharField(
        max_length=8, default='#7b1fa2', blank=True)
    title = models.CharField(max_length=100, default='user')
    website = models.URLField(default='', blank=True)
    gender = models.CharField(
        max_length=3,
        choices=GENDER_CHOICES,
        default='',
        blank=True
    )
    about_me = models.TextField(default='', blank=True)
    account_type = models.CharField(max_length=100, default='personal', blank=True)
    referred_by = models.ForeignKey(User, null=True, blank=True)
    ekata_id = models.CharField(max_length=100, default='', blank=True)

    name_public = models.BooleanField(default=True)
    website_public = models.BooleanField(default=True)
    gender_public = models.BooleanField(default=True)
    business_public = models.BooleanField(default=True)
    location_public = models.BooleanField(default=True)
    avatar_public = models.BooleanField(default=True)
    phone_public = models.BooleanField(default=True)
    completion_public = models.BooleanField(default=True)
    bio_public = models.BooleanField(default=True)
    invitation_verified = models.BooleanField(default=False)
    users_link_visible = models.BooleanField(default=False)
    groups_link_visible = models.BooleanField(default=False)
    timeline_link_visible = models.BooleanField(default=False)
    messaging_link_visible = models.BooleanField(default=False)
    information_link_visible = models.BooleanField(default=False)
    hashtagcampaign_link_visible = models.BooleanField(default=False)

    grantcoin_staff = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username

    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def online(self):
        if cache.get('%s_is_online' % self.user.username):
            return True
        else:
            return False

    def create_profile(sender, **kwargs):
        colors = [
            '#c62828', '#7b1fa2', '#00838f',
            '#2e7d32', '#fbc02d', '#d84315'
        ]
        user = kwargs["instance"]
        if kwargs["created"]:
            user_profile = UserProfile(user=user)
            user_profile.default_avatar_color = random.choice(colors)
            user_profile.save()
    post_save.connect(create_profile, sender=User)

    class Meta:
        verbose_name_plural = 'Profile'


def get_upload_path(instance, filename):
    return 'documents/{0}/{1}'.format(instance.user.username, filename)


class UserDocuments(models.Model):
    user = models.ForeignKey(User)
    document = models.FileField(upload_to=get_upload_path)

    def filename(self):
        return os.path.basename(self.document.name)

    def __unicode__(self):
        return self.filename()


@receiver(post_delete, sender=UserDocuments)
def delete_file(sender, instance, **kwargs):
    if instance.document:
        if os.path.isfile(instance.document.path):
            os.remove(instance.document.path)


class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='address')
    house_number = models.CharField(verbose_name=_('House Number'), max_length=10, default='', blank=True)
    street = models.CharField(verbose_name=_('Street'), max_length=200, default='', blank=True)
    zip_code = models.CharField(verbose_name=_('Zip Code'), max_length=10, default='', blank=True)
    city = models.CharField(verbose_name=_('City'), max_length=100, default='', blank=True)
    state = models.CharField(verbose_name=_('State'), max_length=100, default='', blank=True)
    country = CountryField(verbose_name=_('Country'), max_length=100, default='', blank=True)


class UserPhone(models.Model):
    user = models.OneToOneField(User, related_name='phone')
    phone_office = models.CharField(max_length=20, default='', blank=True)
    phone_home = models.CharField(max_length=20, default='', blank=True)
    phone_mobile = models.CharField(max_length=20, default='', blank=True)
    phone_emergency = models.CharField(max_length=20, default='', blank=True)


class UserCompletionRing(models.Model):
    user = models.OneToOneField(User, related_name='cring')
    skipped_list = JSONField(
        default={'skipped': []}
    )

    def calculate_completed(self):
        emailadd = ""
        profile = self.user.profile
        skipped_tasks = self.skipped_list['skipped']
        completed_tasks = []
        completed = 0
        not_completed = 0
        not_completed_task = []
        if profile.website:
            completed += 1
            completed_tasks.append("website")
        else:
            if "website" not in skipped_tasks:
                not_completed += 1
                not_completed_task.append("website")
        if profile.gender:
            completed += 1
            completed_tasks.append("gender")
        else:
            if "gender" not in skipped_tasks:
                not_completed += 1
                not_completed_task.append("gender")
        if profile.avatar:
            completed += 1
            completed_tasks.append("avatar")
        else:
            if "avatar" not in skipped_tasks:
                not_completed += 1
                not_completed_task.append("avatar")
        if hasattr(self.user, 'phone'):
            completed += 1
            completed_tasks.append("phone")
        else:
            if "phone" not in skipped_tasks:
                not_completed += 1
                not_completed_task.append("phone")
        if hasattr(self.user, 'address'):
            completed += 1
            completed_tasks.append("address")
        else:
            if "address" not in skipped_tasks:
                not_completed += 1
                not_completed_task.append("address")
        if self.user.socialaccount_set.all():
            completed += 1
            completed_tasks.append("socialaccount")
        else:
            if "socialaccount" not in skipped_tasks:
                not_completed += 1
                not_completed_task.append("socialaccount")
        if self.user.emailaddress_set.all():
            completed += 1
            completed_tasks.append("email")
            for emailaddress in self.user.emailaddress_set.all():
                if emailaddress.primary:
                    if emailaddress.verified:
                        completed += 1
                        completed_tasks.append("email_verified")
                    else:
                        if "email_verified" not in skipped_tasks:
                            emailadd = emailaddress.email
                            not_completed += 1
                            not_completed_task.append("email_verified")
                        elif "email_verified" in skipped_tasks:
                            emailadd = emailaddress.email
        else:
            if "email" not in skipped_tasks:
                not_completed += 1
                not_completed_task.append("email")

        return completed, completed_tasks, not_completed, not_completed_task, emailadd

    def calculate_verified(self):
        not_verified = 0
        not_verified_tasks = []
        skipped_tasks = self.skipped_list['skipped']
        if self.user.emailaddress_set.all():
            for emailaddress in self.user.emailaddress_set.all():
                if emailaddress.primary:
                    if not emailaddress.verified and "email_verified" not in skipped_tasks:
                        not_verified += 1
                        not_verified_tasks.append("email_verified")

        return not_verified, not_verified_tasks

    def __unicode__(self):
        return self.user.username


class UserUIState(models.Model):
    user = models.OneToOneField(User, related_name='uistate')
    state = models.TextField()

    def __unicode__(self):
        return self.user.username + "'s state"


class UserOneSignal(models.Model):
    user = models.ForeignKey(User, related_name='onesignals')
    onesignalid = models.CharField(max_length=300)

    def __unicode__(self):
        return self.user.username + "'s onesignal id"


class ReadSysUpdate(models.Model):
    user = models.ForeignKey(User, related_name='readsysupdate')
    sysupdate = models.IntegerField()


def set_unique_id(sender, instance, **kwargs):
    if not instance.ekata_id:
        task_unique_ekata_id_setter.delay(sender, instance)


post_save.connect(set_unique_id, sender=UserProfile)
