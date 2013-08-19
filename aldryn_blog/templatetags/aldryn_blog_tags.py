# -*- coding: utf-8 -*-
from classytags.arguments import Flag
from classytags.core import Options

from django import template

register = template.Library()

from classytags.helpers import InclusionTag

from aldryn_blog.models import Post


class ArchiveNavigation(InclusionTag):
    template = 'aldryn_blog/includes/archive_navigation.html'

    options = Options(
        Flag('full_navigation', true_values=['full_navigation'], default=False),
    )

    def get_context(self, context, **kwargs):
        context['dates'] = Post.published.dates('publication_start', 'month')
        context.update(kwargs)
        return context

register.tag('archive_navigation', ArchiveNavigation)


@register.filter
def posts(latest, objects):
    if latest:
        return latest
    return objects


@register.filter
def user_name(user):
    if user.get_full_name():
        return user.get_full_name()
    return user.username
