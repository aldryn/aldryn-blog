# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_pool import toolbar_pool


@toolbar_pool.register
def blog_toolbar(toolbar, request, is_current_app, app_name):
    if not (is_current_app and request.user.has_perm('aldryn_blog.add_post')):
        return
    menu = toolbar.get_or_create_menu('blog-app', _('Blog'))
    menu.add_modal_item(_('Add Blog Post'), reverse('admin:aldryn_blog_post_add') + '?_popup', close_on_url=reverse('admin:aldryn_blog_post_changelist'))
    if hasattr(request, 'current_aldryn_blog_entry'):
        menu.add_modal_item(_('Edit Blog Post'), reverse('admin:aldryn_blog_post_change', args=(request.current_aldryn_blog_entry.pk,)) + '?_popup', close_on_url=reverse('admin:aldryn_blog_post_changelist'), active=True)
    else:
        menu.add_modal_item(_('Edit Blog Post'), '#', active=False)
    if toolbar.edit_mode:
        switcher = toolbar.add_button_list('Mode Switcher', side=toolbar.RIGHT,
                                           extra_classes=['cms_toolbar-item-cms-mode-switcher'])
        switcher.add_button(_("Content"), '?edit', active=not toolbar.build_mode, disabled=toolbar.build_mode)
        switcher.add_button(_("Structure"), '?build', active=toolbar.build_mode, disabled=not toolbar.build_mode)
