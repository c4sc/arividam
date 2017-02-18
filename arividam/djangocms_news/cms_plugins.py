from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from cms.models import Page
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from arividam.utils import get_page_by_slug
from .models import PromotedNews

import logging

logger = logging.getLogger(__name__)

class NewsPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("News")
    render_template = "djangocms_news/plugin.html"
    cache = False

    def render(self, context, instance, placeholder):
        news = get_page_by_slug('news')
        children = news.children.order_by("-publication_date")[:3]
        pages = [{'title': child.get_title(settings.LANGUAGE_CODE),
            'content': child.get_placeholders()[0].render(context, None),
            'id': child.pk
            } for child in children]
        context.update({
            'news': pages
            })
        return context

class FeaturedNewsPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Featured News")
    render_template = "djangocms_news/featured.html"
    cache = False

    def render(self, context, instance, placeholder):
        site = get_current_site(context['request'])
        news = PromotedNews.objects.filter(site=site).order_by("-page__publication_date")[:5]
        context.update({
            "news": news
        })
        return context

plugin_pool.register_plugin(NewsPlugin)
plugin_pool.register_plugin(FeaturedNewsPlugin)
