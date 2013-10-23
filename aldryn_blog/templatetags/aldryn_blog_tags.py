# -*- coding: utf-8 -*-
from classytags.arguments import Flag
from classytags.core import Options

from django import template

register = template.Library()

@register.filter
def posts(latest, objects):
    if latest:
        return latest
    return objects


@register.filter
def user_name(user):
    if user.get_full_name():
        return user.get_full_name()
    return user.username
