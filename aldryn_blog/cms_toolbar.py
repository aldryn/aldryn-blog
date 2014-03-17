# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from aldryn_blog import request_post_identifier


@toolbar_pool.register
class BlogToolbar(CMSToolbar):
    def populate(self):
        if not (self.is_current_app and self.request.user.has_perm('aldryn_blog.add_post')):
            return
        menu = self.toolbar.get_or_create_menu('blog-app', _('Blog'))
        menu.add_modal_item(_('Add Blog Post'), reverse('admin:aldryn_blog_post_add'))

        blog_entry = getattr(self.request, request_post_identifier, None)
        if blog_entry and self.request.user.has_perm('aldryn_blog.change_post'):
            menu.add_modal_item(_('Edit Blog Post'), reverse('admin:aldryn_blog_post_change', args=(blog_entry.pk,)),
                                active=True)
