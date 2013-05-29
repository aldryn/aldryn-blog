# -*- coding: utf-8 -*-
import copy
from distutils.version import LooseVersion
from django.conf import settings
from django.contrib import admin

import cms
from cms.admin.placeholderadmin import PlaceholderAdmin

from aldryn_blog.models import Post


class PostAdmin(PlaceholderAdmin):
    render_placeholder_language_tabs = False
    list_display = ('title', 'author', 'publication_date')
    date_hierarchy = 'publication_date'
    raw_id_fields = ['author']

    _fieldsets = [
        (None, {
            'fields': ('title', 'slug', 'publication_date', 'author', 'language',)
        }),
        (None, {
            'fields': ('key_visual', 'lead_in', 'tags',)
        }),
        ('Content', {
            'classes': ('plugin-holder', 'plugin-holder-nopage',),
            'fields': ('content',)
        }),
    ]

    def get_fieldsets(self, request, obj=None):
        fieldsets = copy.deepcopy(self._fieldsets)

        # remove language field if only one language is available
        if len(settings.LANGUAGES) <= 1:
            fieldsets[0][1]['fields'] = fieldsets[0][1]['fields'][:-1]

        # remove placeholder field if CMS 3.0
        if LooseVersion(cms.__version__) >= LooseVersion('3.0'):
            del fieldsets[-1]

        return fieldsets

    def get_list_display(self, request):
        if len(settings.LANGUAGES) > 1:
            return self.list_display + ('language',)
        return self.list_display

    def add_view(self, request, *args, **kwargs):
        data = request.GET.copy()
        data['author'] = request.user.id
        request.GET = data
        return super(PostAdmin, self).add_view(request, *args, **kwargs)

admin.site.register(Post, PostAdmin)
