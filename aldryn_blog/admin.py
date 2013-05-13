# -*- coding: utf-8 -*-
from django.contrib import admin

from cms.admin.placeholderadmin import PlaceholderAdmin

from aldryn_blog.models import Post


class PostAdmin(PlaceholderAdmin):

    raw_id_fields = ['author']

    def add_view(self, request, *args, **kwargs):
        data = request.GET.copy()
        data['author'] = request.user.id
        request.GET = data
        return super(PostAdmin, self).add_view(request, *args, **kwargs)

admin.site.register(Post, PostAdmin)
