# -*- coding: utf-8 -*-

from django import template

register = template.Library()

from classytags.helpers import InclusionTag

from aldryn_blog.models import Post


class ArchiveNavigation(InclusionTag):
    template = 'aldryn_blog/snippets/archive_navigation.html'

    def get_context(self, context, **kwargs):
        context['dates'] = Post.published.dates('publication_date', 'month')
        return context

register.tag('archive_navigation', ArchiveNavigation)
