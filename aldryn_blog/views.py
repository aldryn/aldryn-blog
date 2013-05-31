# -*- coding: utf-8 -*-
import datetime
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

    def get_queryset(self):
        qs = super(ArchiveView, self).get_queryset()
        if 'month' in self.kwargs:
            qs = qs.filter(publication_date__month=self.kwargs['month'])
        if 'year' in self.kwargs:
            qs = qs.filter(publication_date__year=self.kwargs['year'])
        return qs

    def get_context_data(self, **kwargs):
        kwargs['year'] = int(self.kwargs.get('year')) if 'year' in self.kwargs else None
        kwargs['month'] = int(self.kwargs.get('month')) if 'month' in self.kwargs else None
        if kwargs['year']:
            kwargs['archive_date'] = datetime.date(kwargs['year'], kwargs['month'] or 1, 1)
        return super(ArchiveView, self).get_context_data(**kwargs)


class TaggedListView(LanguageMixin, ListView):
    model = Post

    def get_queryset(self):
        return super(TaggedListView, self).get_queryset().filter(tags__slug=self.kwargs['tag'])


class PostDetailView(LanguageMixin, PublishMixin, DetailView):

    model = Post
    queryset = Post.objects.select_related('key_visual')

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        if 'post' in response.context_data:
            request.current_aldryn_blog_entry = response.context_data['post']
        return response
