# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar


@toolbar_pool.register
class BlogToolbar(CMSToolbar):
    def populate(self):
        if not (self.is_current_app and self.request.user.has_perm('aldryn_blog.add_post')):
            return
        menu = self.toolbar.get_or_create_menu('blog-app', _('Blog'))
        menu.add_modal_item(_('Add Blog Post'), reverse('admin:aldryn_blog_post_add') + '?_popup',
                            close_on_url=reverse('admin:aldryn_blog_post_changelist'))
        if hasattr(self.request, 'current_aldryn_blog_entry'):
            menu.add_modal_item(_('Edit Blog Post'), reverse('admin:aldryn_blog_post_change', args=(
            self.request.current_aldryn_blog_entry.pk,)) + '?_popup',
                                close_on_url=reverse('admin:aldryn_blog_post_changelist'), active=True)
        else:
            menu.add_modal_item(_('Edit Blog Post'), '#', active=False)
