# -*- coding: utf-8 -*-
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from aldryn_blog.models import Post


class PublishMixin(object):
    def get_allow_future(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class ArchiveView(PublishMixin, ArchiveIndexView):

    model = Post
    queryset = Post.objects.select_related('key_visual')
    date_field = 'publication_date'
    allow_empty = True


class TaggedListView(ListView):
    model = Post

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            qs = Post.objects.all()
        else:
            qs = Post.published.all()
        return qs.filter(tags__slug=self.kwargs['tag'])


class PostDetailView(PublishMixin, DetailView):

    model = Post
    queryset = Post.objects.select_related('key_visual')
