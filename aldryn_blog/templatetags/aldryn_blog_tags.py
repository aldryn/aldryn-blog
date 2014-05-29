# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse

register = template.Library()


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


@register.assignment_tag
def get_blog_post_tags(post):
    """
    Returns a list of tags for post, with an extra url attribute.
    """
    post_tags = list(post.tags.all())

    for tag in post_tags:
        tag.get_absolute_url = reverse('aldryn_blog:tagged-posts', kwargs={'tag': tag.slug})
    return post_tags
