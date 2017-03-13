from __future__ import unicode_literals

import markdown
import bleach

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings

from ckeditor_uploader.fields import RichTextUploadingField
from versatileimagefield.fields import VersatileImageField
from versatileimagefield.placeholder import OnStoragePlaceholderImage

# Create your models here.


class GlobalOgTag(models.Model):
    name = models.CharField(max_length=200, default='', blank=False)
    title = models.CharField(max_length=100, default='', blank=False)
    page_type = models.CharField(max_length=40, default='', blank=False)
    description = models.CharField(max_length=255, default='', blank=False)
    app_id = models.CharField(max_length=40, default='', blank=True)
    image = models.ImageField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class ExtraMetaTag(models.Model):
    ogtag = models.ForeignKey(GlobalOgTag)
    meta_tag = models.CharField(
        max_length=30,
        help_text='enter full og meta name'
    )
    description = models.CharField(max_length=255)

    def __unicode__(self):
        return self.meta_tag


class OgTagLink(models.Model):
    PAGE_CHOICES = (
        ('index', 'index'),
        ('hashtag', 'hashtag'),
        ('news', 'news'),
        ('crowdfunding', 'crowdfunding')
    )
    page = models.CharField(max_length=40, choices=PAGE_CHOICES)
    globalogtag = models.ForeignKey(GlobalOgTag, null=True)

    def __unicode__(self):
        return self.page


class Tags(models.Model):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Tags'


class News(models.Model):
    author = models.ForeignKey(User, related_name='news', editable=False)
    tags = models.ManyToManyField(Tags, related_name='news')
    title = models.CharField(max_length=100)
    content = RichTextUploadingField()
    draft = models.BooleanField(default=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    clickcount = models.IntegerField(editable=False, default=0)
    ogtag = models.ForeignKey(GlobalOgTag, null=True, blank=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('landing:news_detail', args=[self.id, ])

    class Meta:
        verbose_name_plural = 'News'


class HashtagImg(models.Model):
    lat = models.CharField(max_length=40, default='')
    lng = models.CharField(max_length=40, default='')
    uploader = models.CharField(max_length=40, default='')
    image = VersatileImageField(
        upload_to='hashtagimg',
        blank=True,
        null=True
    )

    def __unicode__(self):
        return self.uploader
