from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from cms.models import Page
from django.conf import settings

import logging

logger = logging.getLogger(__name__)

class NewsPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("News")
    render_template = "djangocms_news/plugin.html"
    cache = False

    def render(self, context, instance, placeholder):
        news = Page.objects.search("news")[0]
        children = news.children.order_by("publication_date")
        pages = [{'title': child.get_title(settings.LANGUAGE_CODE),
            'content': child.get_placeholders()[0].render(context, 120)
            } for child in children]
        context.update({
            'news': pages
            })
        return context

plugin_pool.register_plugin(NewsPlugin)
