# -*- coding: utf-8 -*-
import copy
from distutils.version import LooseVersion

from django.conf import settings
from django.contrib import admin

import cms
from cms.admin.placeholderadmin import PlaceholderAdmin, FrontendEditableAdmin
from hvad.admin import TranslatableAdmin

from .forms import PostForm, CategoryForm
from .models import Post, Category


class PostAdmin(FrontendEditableAdmin, PlaceholderAdmin):

    render_placeholder_language_tabs = False
    list_display = ['title', 'author', 'publication_start', 'publication_end']
    date_hierarchy = 'publication_start'
    form = PostForm
    frontend_editable_fields = ('title', 'lead_in')

    _fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'publication_start', 'publication_end', 'author', 'coauthors', 'language']
        }),
        (None, {
            'fields': ['key_visual', 'lead_in', 'category', 'tags']
        }),
        ('Content', {
            'classes': ['plugin-holder', 'plugin-holder-nopage'],
            'fields': ['content']
        }),
    ]

    raw_id_fields = ['author', 'coauthors'] if getattr(settings, 'ALDRYN_BLOG_USE_RAW_ID_FIELDS', False) else []
    filter_horizontal = ['coauthors']

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
            return self.list_display + ['language']
        return self.list_display

    def add_view(self, request, *args, **kwargs):
        data = request.GET.copy()
        data['author'] = request.user.id  # default author is logged-in user
        request.GET = data
        return super(PostAdmin, self).add_view(request, *args, **kwargs)

admin.site.register(Post, PostAdmin)


class CategoryAdmin(TranslatableAdmin):

    form = CategoryForm
    list_display = ['__unicode__', 'all_translations', 'ordering']
    list_editable = ['ordering']

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {'fields': ['name', 'slug']}),
        ]
        return fieldsets

admin.site.register(Category, CategoryAdmin)
