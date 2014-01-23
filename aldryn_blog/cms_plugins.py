# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from aldryn_blog import models
from aldryn_blog.forms import LatestEntriesForm


class BlogPlugin(CMSPluginBase):

    module = 'Blog'


class LatestEntriesPlugin(BlogPlugin):

    render_template = 'aldryn_blog/plugins/latest_entries.html'
    name = _('Latest Blog Entries')
    model = models.LatestEntriesPlugin
    form = LatestEntriesForm

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


class AuthorsPlugin(BlogPlugin):
    render_template = 'aldryn_blog/plugins/authors.html'
    name = _('Blog Authors')
    model = models.AuthorsPlugin
    filter_horizontal = ['authors']

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


class BlogTagsPlugin(BlogPlugin):

    render_template = 'aldryn_blog/plugins/tags.html'
    name = _('Tags')
    model = CMSPlugin

    def render(self, context, instance, placeholder):
        context['tags'] = models.Post.published.get_tags(
            language=instance.language)
        return context


class BlogArchivePlugin(BlogPlugin):

    render_template = 'aldryn_blog/plugins/archive.html'
    name = _('Archive')
    model = CMSPlugin

    def render(self, context, instance, placeholder):
        context['dates'] = models.Post.published.get_months(
            language=instance.language)
        return context


plugin_pool.register_plugin(LatestEntriesPlugin)
plugin_pool.register_plugin(AuthorsPlugin)
plugin_pool.register_plugin(BlogTagsPlugin)
plugin_pool.register_plugin(BlogArchivePlugin)
