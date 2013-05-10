# -*- coding: utf-8 -*-
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.detail import DetailView

from aldryn_blog.models import Post


class ArchiveView(ArchiveIndexView):

    model = Post
    date_field = 'publication_date'


class PostDetailView(DetailView):

    model = Post
