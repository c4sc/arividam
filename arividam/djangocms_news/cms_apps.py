#!/usr/bin/env python
#-*- coding: utf-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

class NewsApphook(CMSApp):
    app_name = "news"
    name = "News Application"
    urls = ['arividam.djangocms_news.urls']

apphook_pool.register(NewsApphook)
