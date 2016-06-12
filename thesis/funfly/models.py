# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from moderation.db import ModeratedModel


# Create your models here.
SEX = (
    ('0', 'Female'),
    ('1', 'Male'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    sex = models.CharField(null=True, max_length=1, default=None, choices=SEX,
        verbose_name=u'Are you male or female?')
    city = models.CharField(null=True, default=None, max_length=100)
    timezone = models.CharField(null=True, default=None, max_length=100)

    def __unicode__(self):
        return u'%s' % self.user


class Ninegag(ModeratedModel):
    title = models.CharField(max_length=100, db_index=True)
    source_url = models.CharField(max_length=200)
    imagevideo_path = models.CharField(max_length=200)
    is_video = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return u'%s' % self.title

    class Moderator:
        notify_user = False
        fields_exclude = ['points', 'date_added']


class Joke(ModeratedModel):
    identifier = models.CharField(max_length=50, default='', db_index=True)
    text = models.TextField(default='')
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    category = models.CharField(max_length=100, null=True, blank=False, default='')

    def __unicode__(self):
        return u'%s' % self.text

    class Moderator:
        notify_user = False
        fields_exclude = ['likes', 'dislikes']


class PostComment(models.Model):
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    # post = models.ForeignKey('Youtube', related_name='comments',
    #                          verbose_name='post', on_delete=models.CASCADE)
    #

    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, related_name='comments',
                             verbose_name='user', on_delete=models.CASCADE)

    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __unicode__(self):
        return u'{} @ {}'.format(self.user, self.date_added)


class Youtube(models.Model):
    identifier = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    added_at = models.DateTimeField(null=True)
    comments = GenericRelation(PostComment, related_query_name='comments')

    def __unicode__(self):
        return u'%s' % self.title

    def get_content_type(self):
        return ContentType.objects.get_for_model(self).id