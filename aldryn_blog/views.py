# -*- coding: utf-8 -*-
import datetime

from django.views.generic.dates import ArchiveIndexView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from aldryn_blog.models import Post


class BasePostView(object):

    def get_queryset(self):
        if self.request.user.is_staff:
            manager = Post.objects
        else:
            manager = Post.published
        return manager.filter_by_current_language()


class ArchiveView(BasePostView, ArchiveIndexView):

    date_field = 'publication_start'
    allow_empty = True
    allow_future = True

    def get_queryset(self):
        qs = super(ArchiveView, self).get_queryset()
        if 'month' in self.kwargs:
            qs = qs.filter(publication_start__month=self.kwargs['month'])
        if 'year' in self.kwargs:
            qs = qs.filter(publication_start__year=self.kwargs['year'])
        return qs

    def get_context_data(self, **kwargs):
        kwargs['month'] = int(self.kwargs.get('month')) if 'month' in self.kwargs else None
        kwargs['year'] = int(self.kwargs.get('year')) if 'year' in self.kwargs else None
        if kwargs['year']:
            kwargs['archive_date'] = datetime.date(kwargs['year'], kwargs['month'] or 1, 1)
        return super(ArchiveView, self).get_context_data(**kwargs)


class TaggedListView(BasePostView, ListView):

    def get_queryset(self):
        qs = super(TaggedListView, self).get_queryset()
        return qs.filter(tags__slug=self.kwargs['tag'])


class PostDetailView(BasePostView, DetailView):

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        if 'post' in response.context_data:
            request.current_aldryn_blog_entry = response.context_data['post']
        return response
