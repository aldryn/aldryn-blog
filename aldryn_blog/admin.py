# -*- coding: utf-8 -*-
from django.contrib import admin

from cms.admin.placeholderadmin import PlaceholderAdmin

from aldryn_blog.models import Post


class PostAdmin(PlaceholderAdmin):

    pass

admin.site.register(Post, PostAdmin)
