# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from cms.models.fields import PlaceholderField
from cms.models.pluginmodel import CMSPlugin

import datetime
from taggit.managers import TaggableManager


class Post(models.Model):

    title = models.CharField(_('Title'), max_length=255)
    slug = models.CharField(_('Slug'), max_length=255, unique=True, blank=True,
                            help_text=_('Used in the URL. If changed, the URL will change. '
                                        'Clean it to have it re-created.'))
    content = PlaceholderField('blog_post_content')
    author = models.ForeignKey(User)
    publication_date = models.DateField(default=datetime.date.today,
                                        help_text=_('Used in the URL. If changed, the URL will change.'))

    objects = models.Manager()
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {'year': self.publication_date.year,
                  'month': self.publication_date.month,
                  'day': self.publication_date.day,
                  'slug': self.slug}
        return reverse('aldryn-blog:post-detail', kwargs=kwargs)

    class Meta:
        ordering = ['-publication_date']

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Post, self).save()


class LastEntriesPlugin(CMSPlugin):

    last_entries_number = models.IntegerField()

    def __unicode__(self):
        return u'%s' % (self.last_entries_number,)

    def get_posts(self):
        return Post.objects.filter(publication_date__lte=datetime.date.today())[:self.last_entries_number]
