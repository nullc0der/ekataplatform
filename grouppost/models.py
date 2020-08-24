from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from versatileimagefield.fields import VersatileImageField

# Create your models here.

# TODO: Move other post related models from groupsystem to here


class PostImage(models.Model):
    uploader = models.ForeignKey(User)
    image = VersatileImageField(upload_to='group_post_images')
