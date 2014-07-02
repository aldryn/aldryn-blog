# -*- coding: utf-8 -*-
import datetime

from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils.translation import ugettext as _, get_language

from aldryn_blog.models import Post


class LatestEntriesFeed(Feed):

    def link(self):
        return reverse('aldryn_blog:latest-posts')

    def title(self):
        return _('Blog posts on %(site_name)s') % {'site_name': Site.objects.get_current().name}

    def items(self, obj):
        return Post.published.filter(
            Q(language=get_language()) | Q(language__isnull=True)
        ).order_by('-publication_start')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.lead_in

    def item_pubdate(self, item):
        return datetime.datetime.combine(item.publication_start, datetime.time())


class TagFeed(LatestEntriesFeed):

    def get_object(self, request, tag):
        return tag

    def items(self, obj):
        return Post.published.filter(tags__slug=obj)[:10]


class CategoryFeed(LatestEntriesFeed):

    def get_object(self, request, category):
        return category

    def items(self, obj):
        return Post.published.filter(category__slug=obj)[:10]
