# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

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


class AuthorEntriesPlugin(BlogPlugin):
    render_template = 'aldryn_blog/plugins/author_entries.html'
    name = _('Author Blog Entries')
    model = models.AuthorEntriesPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


plugin_pool.register_plugin(LatestEntriesPlugin)
plugin_pool.register_plugin(AuthorEntriesPlugin)
