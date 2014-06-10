# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from aldryn_blog.views import (
    ArchiveView, PostDetailView, TaggedListView, AuthorEntriesView,
    TagsListView, AuthorsListView, CategoryListView, CategoryPostListView)
from aldryn_blog.feeds import LatestEntriesFeed, TagFeed, CategoryFeed

urlpatterns = patterns(
    '',
    url(r'^$', ArchiveView.as_view(), name='latest-posts'),
    url(r'^author/$', AuthorsListView.as_view(), name='author-list'),
    url(r'^author/(?P<slug>[\w.@+-]+)/$', AuthorEntriesView.as_view(), name='author-posts'),
    url(r'^feed/$', LatestEntriesFeed(), name='latest-posts-feed'),
    url(r'^(?P<year>\d{4})/$', ArchiveView.as_view(), name='archive-year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', ArchiveView.as_view(), name='archive-month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', ArchiveView.as_view(), name='archive-day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>\w[-\w]*)/$', PostDetailView.as_view(), name='post-detail'),
    url(r'^category/$', CategoryListView.as_view(), name='category-list'),
    url(r'^category/(?P<category>[-\w]+)/$', CategoryPostListView.as_view(), name='category-posts'),
    url(r'^category/(?P<category>[-\w]+)/feed/$', CategoryFeed(), name='category-posts-feed'),
    url(r'^tag/$', TagsListView.as_view(), name='tag-list'),
    url(r'^tag/(?P<tag>[-\w]+)/$', TaggedListView.as_view(), name='tagged-posts'),
    url(r'^tag/(?P<tag>[-\w]+)/feed/$', TagFeed(), name='tagged-posts-feed'),
)
