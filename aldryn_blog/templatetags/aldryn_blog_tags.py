# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse

from ..models import Post


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


@register.assignment_tag
def get_related_posts(post, by_categories=True, by_tags=True, by_latest=True, wanted_count=5):
    """
    Returns a list of blog objects being related to the one given.

    "Related" can mean one or multiple of the following conditions
    (being configurable by the arguments passed to this function):
     - In the same category
     - Having one or more tags in common
     - Just being released recently

    Another rule to follow:
     - found_objects == wanted_count => return found_objects
     - found_objects < wanted_count => fill the missing count with the next condition
     - found_objects > wanted_count => further trim down found_objects by the next condition
    """

    given_category = post.category_id
    given_tags = post.tags.values_list('pk', flat=True)
    given_language = post.language

    found = None
    all_posts = Post.objects.filter(language=given_language).order_by('publication_start')

    if by_categories:
        posts_by_category = all_posts.filter(category_id=given_category)

        if posts_by_category.count() == wanted_count:
            return list(posts_by_category)

        found = posts_by_category

    if by_tags:
        append = False
        if found:
            if found.count() > wanted_count:
                qs = found
            else:
                append = True
                qs = all_posts
            found = list(found)
        else:
            qs = all_posts

        posts_by_tags = list(qs.filter(tags__in=given_tags).exclude(id__in=[p.id for p in found]))

        if posts_by_tags:
            if append:
                found += posts_by_tags
            else:
                found = posts_by_tags

            if len(found) >= wanted_count:
                return posts_by_tags[:wanted_count]

    if by_latest:
        if not found:
            found = []
        return found + list(all_posts.exclude(id__in=[p.id for p in found])[:wanted_count - len(found)])

    return found
