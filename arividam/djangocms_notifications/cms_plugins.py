from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from cms.models import Page

import logging

logger = logging.getLogger(__name__)

class NotificationsPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Notifications List")
    render_template = "djangocms_notifications/plugin.html"
    cache = False

    def render(self, context, instance, placeholder):
        try:
            notifications = Page.objects.search("notification")[0]
        except IndexError:
            notifications = None
        context.update({ 'notifications': notifications })
        return context


plugin_pool.register_plugin(NotificationsPlugin)
