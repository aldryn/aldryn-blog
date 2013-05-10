# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from aldryn_blog import models


class BlogPlugin(CMSPluginBase):

    module = 'Blog'


class LastEntriesPlugin(BlogPlugin):

    render_template = 'aldryn_blog/last_entries.html'
    name = _('Last Blog Entries')
    model = models.LastEntriesPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context

plugin_pool.register_plugin(LastEntriesPlugin)
