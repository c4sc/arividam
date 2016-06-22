# -*- coding: utf-8 -*-
from ajax_select import register, LookupChannel
from django.contrib.auth.models import Group

from .models import User

@register('users')
class UserLookup(LookupChannel):
    model = User

    def get_query(self, q, request):
        return self.model.objects.filter(username=q)

    def format_item_display(self, item):
        return u"<span class='user'>{}</span>".format(item.username)

@register('groups')
class GroupLookup(LookupChannel):
    model = Group

    def get_query(self, q, request):
        return self.model.objects.filter(name=q)

    def format_item_display(self, item):
        return u"<span class='group'>{}</span>".format(item.username)



