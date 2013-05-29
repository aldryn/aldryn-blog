# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import get_language
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from aldryn_blog.models import Post


class LanguageMixin(object):
    def get_queryset(self):
        return super(LanguageMixin, self).get_queryset().filter(
            models.Q(language__isnull=True) | models.Q(language=get_language()),
        )


class PublishMixin(object):
    def get_allow_future(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class ArchiveView(LanguageMixin, PublishMixin, ArchiveIndexView):

    model = Post
    queryset = Post.objects.select_related('key_visual')
    date_field = 'publication_date'
    allow_empty = True


class TaggedListView(LanguageMixin, ListView):
    model = Post

    def get_queryset(self):
        return super(TaggedListView, self).get_queryset().filter(tags__slug=self.kwargs['tag'])


class PostDetailView(LanguageMixin, PublishMixin, DetailView):

    model = Post
    queryset = Post.objects.select_related('key_visual')

