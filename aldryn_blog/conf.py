# -*- coding: utf-8 -*-

from django.conf import settings
from appconf import AppConf


class AldrynBlogAppConf(AppConf):
    PLUGIN_LANGUAGE = settings.LANGUAGES[0][0]
    SEARCH = True

    class Meta:
        prefix = 'ALDRYN_BLOG'
