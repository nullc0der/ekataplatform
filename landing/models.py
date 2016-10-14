from __future__ import unicode_literals

import markdown
import bleach

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings

from markdownx.models import MarkdownxField
from versatileimagefield.fields import VersatileImageField
from versatileimagefield.placeholder import OnStoragePlaceholderImage

# Create your models here.


class Tags(models.Model):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Tags'


class News(models.Model):
    author = models.ForeignKey(User, related_name='news')
    tags = models.ManyToManyField(Tags, related_name='news')
    title = models.CharField(max_length=100)
    content = MarkdownxField()
    draft = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    clickcount = models.IntegerField(editable=False, default=0)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.content:
            html = markdown.markdown(self.content)
            html_sanitized = bleach.clean(
                html,
                settings.BLEACH_VALID_TAGS,
                settings.BLEACH_VALID_ATTRS,
                settings.BLEACH_VALID_STYLES
            )
            self.content = html_sanitized
        super(News, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('landing:news_detail', args=[self.id, ])

    class Meta:
        verbose_name_plural = 'News'


class NewsOgTag(models.Model):
    news = models.OneToOneField(News)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField()

    def __unicode__(self):
        return self.title


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


class OgTag(models.Model):
    PAGE_CHOICES = (
        ('index', 'index'),
        ('hashtag', 'hashtag'),
        ('news', 'news')
    )
    page = models.CharField(max_length=10, choices=PAGE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField()

    def __unicode__(self):
        return self.page
