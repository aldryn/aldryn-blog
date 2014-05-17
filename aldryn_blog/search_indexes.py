# -*- coding: utf-8 -*-
from django.db.models import Q
from django.template import RequestContext

from aldryn_search.utils import get_index_base, strip_tags

from .conf import settings
from .models import Post


class BlogIndex(get_index_base()):
    haystack_use_for_indexing = settings.ALDRYN_BLOG_SEARCH

    INDEX_TITLE = True

    def get_title(self, obj):
        return obj.title

    def get_description(self, obj):
        return obj.lead_in

    def get_language(self, obj):
        return obj.language

    def prepare_pub_date(self, obj):
        return obj.publication_start

    def get_index_queryset(self, language):
        queryset = self.get_model().published.all()
        return queryset.filter(Q(language=language)|Q(language__isnull=True))

    def get_model(self):
        return Post

    def get_search_data(self, obj, language, request):
        lead_in = self.get_description(obj)
        text_bits = [strip_tags(lead_in)]
        plugins = obj.content.cmsplugin_set.filter(language=language)
        for base_plugin in plugins:
            instance, plugin_type = base_plugin.get_plugin_instance()
            if not instance is None:
                content = strip_tags(instance.render_plugin(context=RequestContext(request)))
                text_bits.append(content)
        return ' '.join(text_bits)
