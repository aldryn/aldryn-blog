# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.toolbar.items import Item, List
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool


class BlogToolbar(CMSToolbar):
    def insert_items(self, items, toolbar, request, is_app):
        self.is_app = is_app
        self.request = request

        self.toolbar = toolbar
        self.can_change = True  # TODO fix
        toolbar.can_change = self.can_change
        menu_items = List('#', _('Blog'))
        menu_items.items.append(Item(reverse('admin:aldryn_blog_post_add') + '?_popup', _('Add Blog Entry'), load_modal=True, active=True))
        if hasattr(request, 'current_aldryn_blog_entry'):
            menu_items.items.append(Item(reverse('admin:aldryn_blog_post_change', args=(self.request.current_aldryn_blog_entry.pk,)) + '?_popup', _('Edit Blog Entry'), load_modal=True))
        else:
            menu_items.items.append(Item('#', _('Edit Blog Enty'), load_modal=True, disabled=True))
        items.append(menu_items)
        return items


toolbar_pool.register(BlogToolbar)
