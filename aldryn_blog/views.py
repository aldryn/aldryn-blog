# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.core.urlresolvers import reverse, resolve
from django.db.models import Q
from django.utils.translation import override, get_language
from django.views import generic
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.utils import timezone

from menus.utils import set_language_changer
from aldryn_blog import request_post_identifier

from aldryn_blog.models import Post


class BasePostView(object):

    def get_queryset(self):
        if self.request.user.is_staff:
            manager = Post.objects
        else:
            manager = Post.published
        return manager.filter_by_current_language()

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['current_app'] = resolve(self.request.path).namespace
        return super(BasePostView, self).render_to_response(context, **response_kwargs)


class ArchiveView(BasePostView, ArchiveIndexView):

    date_field = 'publication_start'
    allow_empty = True
    allow_future = True

    def get_queryset(self):
        qs = BasePostView.get_queryset(self)
        if 'day' in self.kwargs:
            qs = qs.filter(publication_start__day=self.kwargs['day'])
        if 'month' in self.kwargs:
            qs = qs.filter(publication_start__month=self.kwargs['month'])
        if 'year' in self.kwargs:
            qs = qs.filter(publication_start__year=self.kwargs['year'])
        return qs

    def get_context_data(self, **kwargs):
        kwargs['day'] = int(self.kwargs.get('day')) if 'day' in self.kwargs else None
        kwargs['month'] = int(self.kwargs.get('month')) if 'month' in self.kwargs else None
        kwargs['year'] = int(self.kwargs.get('year')) if 'year' in self.kwargs else None
        if kwargs['year']:
            kwargs['archive_date'] = datetime.date(
                kwargs['year'], kwargs['month'] or 1, kwargs['day'] or 1)
        return super(ArchiveView, self).get_context_data(**kwargs)


class AuthorsListView(generic.ListView):
    template_name = 'aldryn_blog/author_list.html'

    def get_queryset(self):
        now = timezone.now()
        authors = User.objects.filter(
            (Q(post__publication_end__isnull=True) | Q(post__publication_end__gte=now))
            & (Q(post__language=get_language()) | Q(post__language__isnull=True))
            & Q(post__publication_start__lte=now)
        ).distinct()
        return authors


class AuthorEntriesView(BasePostView, ListView):

    def get_queryset(self):
        qs = BasePostView.get_queryset(self)
        if 'username' in self.kwargs:
            qs = qs.filter(author__username=self.kwargs['username'])
        return qs

    def get_context_data(self, **kwargs):
        if 'username' in self.kwargs:
            try:
                user = User.objects.get(username=self.kwargs.get('username'))
            except User.DoesNotExist:
                user = None
            kwargs['author'] = user
        return super(AuthorEntriesView, self).get_context_data(**kwargs)


class TagsListView(generic.ListView):
    template_name = 'aldryn_blog/tag_list.html'

    def get_queryset(self):
        return Post.published.get_tags(get_language())


class TaggedListView(BasePostView, ListView):

    def get_queryset(self):
        qs = super(TaggedListView, self).get_queryset()
        return qs.filter(tags__slug=self.kwargs['tag'])

    def get_context_data(self, **kwargs):
        kwargs['tagged_entries'] = (self.kwargs.get('tag')
                                    if 'tag' in self.kwargs else None)
        return super(TaggedListView, self).get_context_data(**kwargs)


def post_language_changer(language):
    with override(language):
        try:
            return reverse('aldryn_blog:latest-posts', )
        except:
            return '/%s/' % language


class PostDetailView(BasePostView, DetailView):
    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        post = response.context_data.get('post', None)
        if post:
            setattr(request, request_post_identifier, post)
            if post.language:
                set_language_changer(request, post_language_changer)
        return response

    def get_context_data(self, **kwargs):
        kwargs['placeholder_language'] = settings.ALDRYN_BLOG_PLUGIN_LANGUAGE or settings.LANGUAGES[0][0]
        return super(PostDetailView, self).get_context_data(**kwargs)
