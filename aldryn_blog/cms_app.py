# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class BlogApp(CMSApp):
    name = _('Blog')
    urls = ['aldryn_blog.urls']
    app_name = 'aldryn_blog'

apphook_pool.register(BlogApp)
