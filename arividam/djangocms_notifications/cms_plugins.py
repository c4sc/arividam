from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from cms.models import Page
from arividam.utils import get_page_by_slug

import logging

logger = logging.getLogger(__name__)

class NotificationsPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Notifications List")
    render_template = "djangocms_notifications/plugin.html"
    cache = False

    def render(self, context, instance, placeholder):
        notifications = get_page_by_slug('notifications')
        context.update({ 'notifications': notifications.children.order_by('-publication_date')[:10] })
        return context

class MarqueePlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Notifications Marquee")
    render_template = "djangocms_notifications/marquee.html"
    cache = True

    def render(self, context, instance, placeholder):
        notifications = get_page_by_slug("notifications")
        context.update({ "notifications": notifications.children.order_by('-publication_date')[:10] })
        return context

plugin_pool.register_plugin(NotificationsPlugin)
plugin_pool.register_plugin(MarqueePlugin)
