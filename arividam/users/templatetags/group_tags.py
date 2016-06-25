#-*- coding: utf-8 -*-

from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    if user.is_superuser:
        return True
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False
    return True if group in user.groups.all() else False

